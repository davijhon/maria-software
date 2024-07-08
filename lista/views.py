import os
import io
import json
import pprint
import boto3
import botocore
from settings import prod

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.conf import settings
from mailmerge import MailMerge
from django.contrib import messages
from django.views.generic import View, ListView
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
from .utils import (
    date2words,
    listado_cumple_no_cumple,
    make_list_pts_cotejo,
    json_deserializer,
)


from .models import PuntosListaCotejo, ResolucionBase, ListaCotejo, Version

from .forms import (
    ResolutionsForm,
)

from .constants import *


# Initializated s3
s3 = boto3.resource(
    "s3",
    aws_access_key_id=prod.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=prod.AWS_SECRET_ACCESS_KEY,
)

bucket = s3.Bucket(prod.AWS_STORAGE_BUCKET_NAME)


class IndexView(LoginRequiredMixin, ListView):
    model = ListaCotejo
    template_name = "lista/index.html"
    context_object_name = "listas_cotejos"
    login_url = "accounts/login/"


class ResolutionGenerator(LoginRequiredMixin, View):
    """
    Muestra el formulario para una lista
    de cotejo seleccionada, y en base a la version escogida.
    La informacion procedente del formulario
    es procesada para generar una acta, entre;
    Cumplimiento Total, Cumplimiento Parcial, Rebeldia.
    """

    pk = None
    version = None

    # Campos que irán en mayuscula, dentro
    # del documento final generado.
    uppercases_fields = [
        "nombre_establecimiento",
        "numero_orden_verificacion",
        "recibio_visita",
        "compareciente",
        "tipo_de_compareciente",
        "iniciales",
        "giro",
        "personalidad_como",
        "aparecen_datos",
        "numero_orden_verificacion_cabosca",
        "numero_orden_verificacion_csscp",
        "fraccion_103",
        "autorizados_oir_recibir",
    ]

    # Campos que irán en miniscula, dentro
    # del documento final generado.
    lower_fields = ["tipo_documento"]

    # Campos que irán capitalizados(Primera letra en mayuscula),
    # dentro del docyument final generado
    capitalize_fields = ["puesto"]

    # Referencia de campos que
    # estan relacionados a fechas.
    #
    # Es necesario tener una referencia,
    # dado que se necesitan desprender,
    # 3 tipos de campos diferentes.
    # para el dia, el mes y el año.
    fechas_fields = [
        "fecha_actual",
        "fecha_orden_visita",
        "fecha_practico_visita",
        "fecha_que_comparece",
        "fecha_desde_acude_comparecer",
        "fecha_hasta_acude_comparecer",
        "fecha_notarial",
    ]

    datetimes = ["dia", "año", "mes"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, slug, pk, *args, **kwargs):
        self.pk = pk
        self.version = Version.objects.get(slug=slug)

        return super().dispatch(request, slug, pk, *args, **kwargs)

    def get(self, request, slug, pk, *args, **kwargs):

        initial = self.get_conditional_objeto_alcance()

        form = ResolutionsForm(initial=initial)

        lista_cotejo_object = ListaCotejo.objects.get(pk=self.pk)
        list_content = PuntosListaCotejo.objects.filter(
            lista_cotejo__pk=self.pk, version=False
        )

        context = {
            "lista_cotejo_object": lista_cotejo_object,
            "form": form,
            "list_content": list_content,
            "version_name": self.version.nombre_version,
            "version": slug,
        }
        return render(self.request, "lista/form.html", context)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(self.request.body)
        data = json_deserializer(json_data["parameters"])
        form = ResolutionsForm(data)
        resolution = ResolucionBase.objects.get(pk=data["resolucion"])

        if form.is_valid():
            cleaned_data = form.cleaned_data

            form_fields = self.form_fields_distribution(cleaned_data)

            form_fields["nombre_lista_cotejo"] = data["lista_cotejo_name"]

            # Se dividen los puntos seleccionados en la lista de cotejo, en el form.
            puntos_cumple_no_cumple, puntos_no_cumple, puntos_cumple = (
                make_list_pts_cotejo(data.items())
            )

            nombre_lista_cotejo = data["lista_cotejo_name"]

            # Se generan listados de numeros separados por comas.
            str_puntos_cumple_no_cumple = listado_cumple_no_cumple(
                puntos_cumple_no_cumple
            )
            str_puntos_no_cumple = listado_cumple_no_cumple(puntos_no_cumple)
            str_puntos_cumple = listado_cumple_no_cumple(puntos_cumple)
            # Se realiza un query, de los puntos
            # seleccionados como no cumple de la lista de
            # cotejo seleccionada.
            # Los mismo seran utilizados para
            # generar una tabla en la plantilla.
            p_list = PuntosListaCotejo.objects.filter(pk__in=puntos_no_cumple)

            # Causa no acredito # Solo para Cumplimiento Parcial
            if resolution.name == "Cumplimiento Parcial":
                try:
                    form_fields["no_acredito_cumplimiento"] = data[
                        "no_acredito_cumplimiento"
                    ]
                except KeyError as e:
                    # No se marcó con check
                    # TODO
                    pass

            # Seleccion de tipo de Documento
            if resolution.name == "Rebeldia":
                docx = self.make_rebeldia_merge_docx(
                    resolution,
                    form_fields,
                    p_list,
                    nombre_lista_cotejo,
                    str_puntos_no_cumple,
                    data,
                )
            elif resolution.name == "Cumplimiento Parcial":
                docx = self.make_parcial_merge_docx(
                    resolution,
                    form_fields,
                    str_puntos_no_cumple,
                    str_puntos_cumple,
                    str_puntos_cumple_no_cumple,
                    nombre_lista_cotejo,
                    p_list,
                    data,
                )
            else:
                docx = self.make_total_merge_docx(
                    resolution,
                    form_fields,
                    str_puntos_cumple_no_cumple,
                    str_puntos_cumple,
                    nombre_lista_cotejo,
                    data,
                )

            if isinstance(docx, type(dict())):
                if docx["error"] == 400:
                    return JsonResponse(
                        {"error": "Ha ocurrido un error al comunicarse con el bucket."},
                        status=400,
                    )
                elif docx["error"] == 404:
                    return JsonResponse(
                        {"error": "No se ha encontrado la ruta del documento."},
                        status=404,
                    )

            response = HttpResponse(docx)
            response["Content-Disposition"] = "attachment; filename=Acta.docx"
            response["Content-Type"] = (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            return response

        return JsonResponse(
            {"error": "No se ha procesado la informacion de forma correcta."},
            status=500,
        )

    def make_rebeldia_merge_docx(
        self,
        resolution,
        form_fields,
        p_list,
        nombre_lista_cotejo,
        str_puntos_no_cumple,
        data,
    ):
        # Devuelve un docx
        # para campos especificos para
        # un acta de tipo `Rebeldia`.
        docx = io.BytesIO()
        tipo_acta = resolution.name.replace(" ", "_")
        data_to_table = list()
        form_fields["str_puntos_no_cumple"] = str_puntos_no_cumple

        # TODO refactorizar.
        if settings.DEBUG:
            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )
            file_path = os.path.join(BASE_DIR, path)

            if os.path.exists(file_path):
                document = MailMerge(file_path)

            else:
                dict_data = {}
                dict_data["error"] = 404
                return dict_data

        else:
            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )

            try:
                s3.Object(prod.AWS_STORAGE_BUCKET_NAME, path).load()
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    dict_data = {}
                    dict_data["error"] = 404
                    return dict_data
                else:
                    dict_data = {}
                    dict_data["error"] = 400
                    return dict_data
            else:

                f_object = bucket.Object(path)
                object_as_streaming_body = f_object.get()["Body"]
                object_as_bytes = object_as_streaming_body.read()
                object_as_file_like = io.BytesIO(object_as_bytes)

                document = MailMerge(object_as_file_like)

        # TODO refactorizar. Será posible crear una clase que maneje todas estas funcione? como metodo??
        form_fields = self.get_conditional_secretaria_salud(
            form_fields, nombre_lista_cotejo
        )
        form_fields = self.get_conditional_informacional_laboral(form_fields)
        form_fields = self.get_conditional_individualizacion_sancion(form_fields)

        # Estructura del Merge Field ===================#
        document.merge(**form_fields)
        # Se crean la estructura para
        # la tabla.
        for p in p_list:
            row = {
                "numero_punto": str(p.numero_punto),
                "punto_acta": p.punto_acta,
                "fundamento_legal": p.fundamento_legal,
                "como_subsanar": p.como_subsanar,
            }
            data_to_table.append(row)

        document.merge_rows("numero_punto", data_to_table)
        document.write(docx)
        document.close()
        docx.seek(0)
        return docx

    def make_parcial_merge_docx(
        self,
        resolution,
        form_fields,
        str_puntos_no_cumple,
        str_puntos_cumple,
        str_puntos_cumple_no_cumple,
        nombre_lista_cotejo,
        p_list,
        data,
    ):
        # Devuelve un docx
        # para campos especificos para
        # un acta de tipo `Cumplimiento Parcial`.
        docx = io.BytesIO()

        tipo_acta = resolution.name.replace(" ", "_")
        data_to_table = list()
        form_fields["str_puntos_no_cumple"] = str_puntos_no_cumple
        form_fields["str_puntos_cumple"] = str_puntos_cumple
        form_fields["str_puntos_cumple_no_cumple"] = str_puntos_cumple_no_cumple

        if settings.DEBUG:
            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )
            file_path = os.path.join(BASE_DIR, path)

            if os.path.exists(file_path):
                document = MailMerge(file_path)

            else:
                dict_data = {}
                dict_data["error"] = 404
                return dict_data
        else:

            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )

            try:
                s3.Object(prod.AWS_STORAGE_BUCKET_NAME, path).load()
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    dict_data = {}
                    dict_data["error"] = 404
                    return dict_data
                else:
                    dict_data = {}
                    dict_data["error"] = 400
                    return dict_data
            else:

                f_object = bucket.Object(path)
                object_as_streaming_body = f_object.get()["Body"]
                object_as_bytes = object_as_streaming_body.read()
                object_as_file_like = io.BytesIO(object_as_bytes)

                document = MailMerge(object_as_file_like)

        form_fields = self.get_conditional_secretaria_salud(
            form_fields, nombre_lista_cotejo
        )
        form_fields = self.get_conditional_documentos(form_fields)
        form_fields = self.get_conditional_parrafo_oir_recibir(form_fields, data)
        form_fields = self.get_conditional_notification_electronica(form_fields)
        form_fields = self.get_conditional_informacional_laboral(form_fields)
        form_fields = self.get_conditional_causas_no_acredito(form_fields)
        form_fields = self.get_conditional_individualizacion_sancion(form_fields)

        document.merge(**form_fields)

        # Se crean la estructura para
        # la tabla.
        for p in p_list:
            row = {
                "numero_punto": str(p.numero_punto),
                "punto_acta": p.punto_acta,
                "fundamento_legal": p.fundamento_legal,
                "como_subsanar": p.como_subsanar,
            }
            data_to_table.append(row)

        document.merge_rows("numero_punto", data_to_table)
        document.write(docx)
        document.close()
        docx.seek(0)
        return docx

    def make_total_merge_docx(
        self,
        resolution,
        form_fields,
        str_puntos_cumple_no_cumple,
        str_puntos_cumple,
        nombre_lista_cotejo,
        data,
    ):
        # Devuelve un docx
        # para campos especificos para
        # un acta de tipo `Cumplimiento Total`.
        docx = io.BytesIO()
        tipo_acta = resolution.name.replace(" ", "_")
        data_to_table = list()
        form_fields["str_puntos_cumple_no_cumple"] = str_puntos_cumple_no_cumple
        form_fields["str_puntos_cumple"] = str_puntos_cumple

        if settings.DEBUG:
            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )
            file_path = os.path.join(BASE_DIR, path)

            if os.path.exists(file_path):
                document = MailMerge(file_path)

            else:
                dict_data = {}
                dict_data["error"] = 404
                return dict_data
        else:
            path = "Plantillas Bases/{lista_cotejo}/{tipo_acta}.docx".format(
                lista_cotejo=nombre_lista_cotejo, tipo_acta=tipo_acta
            )

            try:
                s3.Object(prod.AWS_STORAGE_BUCKET_NAME, path).load()
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    dict_data = {}
                    dict_data["error"] = 404
                    return dict_data
                else:
                    dict_data = {}
                    dict_data["error"] = 400
                    return dict_data
            else:

                f_object = bucket.Object(path)
                object_as_streaming_body = f_object.get()["Body"]
                object_as_bytes = object_as_streaming_body.read()
                object_as_file_like = io.BytesIO(object_as_bytes)

                document = MailMerge(object_as_file_like)

            form_fields = self.get_conditional_secretaria_salud(
                form_fields, nombre_lista_cotejo
            )
            form_fields = self.get_conditional_notification_electronica(form_fields)
            form_fields = self.get_conditional_documentos(form_fields)
            form_fields = self.get_conditional_parrafo_oir_recibir(form_fields, data)
            form_fields = self.get_conditional_individualizacion_sancion(form_fields)

            # Estructura del Merge Field #
            document.merge(**form_fields)
            document.write(docx)
            document.close()
            docx.seek(0)
            return docx

    def form_fields_distribution(self, cleaned_data):
        """
        Devuelve un diccionario con los diferentes
        campos distribuidos segun su formato. Cada campo necesita
        un formato especifico. Asi que se evaluan
        dependiendo de su nombre, y se les da
        formato segun cada condicional.
        """
        form_fields = dict()
        cd = cleaned_data

        # Se itera cada key:value en el diccionario.
        for k, v in cd.items():

            if k in self.fechas_fields:
                # Si el key se encuentra en las lista de fechas.
                # Se utiliza el nombre del campo, para componer
                # 3 variables nuevas, para el dia, mes y año.
                #
                # E.g:
                # Si el campo entrante es `dia_actual: 8/10/1994`
                # se generan 3 nuevos campos, dentro del form_fields,
                # con la siguiente estructura:
                # form_fields = {
                # 		'dia_actual': ocho,
                # 		'mes_actual': octubre,
                # 		'año_actual': mil novecientos noventa y cuatro,
                # }

                extent = k.partition("_")
                # Se transforman el `datetime` en palabras `string`
                d, a, m = date2words(cd[k])
                dates = (d, a, m)
                for i in range(0, len(self.datetimes)):
                    if i == 2:
                        m = dates[i]
                        form_fields[f"{self.datetimes[i]}_{extent[2]}"] = m.lower()
                    else:
                        form_fields[f"{self.datetimes[i]}_{extent[2]}"] = dates[i]

            elif k in self.uppercases_fields:
                form_fields[k] = v.upper()

            elif k in self.lower_fields:
                form_fields[k] = v.lower()

            elif k in self.capitalize_fields:
                form_fields[k] = v.capitalize()

            elif k == "personalidad":
                if v == "Si reconocer":
                    form_fields[k] = "reconocer"
                else:
                    form_fields[k] = "no reconocer"

            elif k == "personalidad_como":
                if v != "":
                    form_fields["personalidad_como"] = v.upper()

            elif k == "personalidad_como_otro":
                if v != "":
                    form_fields["personalidad_como"] = v.upper()

            elif k == "aparecen_datos":
                if v != "":
                    form_fields["aparecen_datos"] = v.upper()

            elif k == "aparecen_datos_otro":
                if v != "":
                    form_fields["aparecen_datos"] = v.upper()

            else:
                form_fields[k] = v

        # Seleccion del tipo de orden CABOSCA | CSSCP
        if form_fields["tipo_orden"] == "AGEPSA/CABOSCA/":
            form_fields["numero_orden_verificacion"] = form_fields[
                "numero_orden_verificacion_cabosca"
            ]
            form_fields["num_fraccion"] = "16"
            form_fields["fraccion_16_or_17"] = form_fields["fraccion_16"]
            form_fields["linea_cabosca_csscp"] = LINEA_CABOSCA

        elif form_fields["tipo_orden"] == "CSSCP/":
            form_fields["numero_orden_verificacion"] = form_fields[
                "numero_orden_verificacion_csscp"
            ]
            form_fields["num_fraccion"] = "17"
            form_fields["fraccion_16_or_17"] = form_fields["fraccion_17"]
            form_fields["linea_cabosca_csscp"] = LINEA_CSSCP

        # Modificacion numero de dia UN|UNO.
        if form_fields["dia_orden_visita"] == "un":
            form_fields["dia_orden_visita"] = "uno"

        if form_fields["dia_practico_visita"] == "un":
            form_fields["dia_practico_visita"] = "uno"

        if form_fields["dia_que_comparece"] == "un":
            form_fields["dia_que_comparece"] = "uno"

        return form_fields

    def get_conditional_secretaria_salud(self, form_fields, nombre_lista_cotejo):
        # Devuelve en el form_fields, los campos
        # corrspondientes para el MergeField,
        # Secretaria Salud.

        # Condicionales. Secretaria Salud ==================================#
        if nombre_lista_cotejo == "Covid-19":
            if form_fields["secretaria_salud"] != "No requiere":
                if form_fields["secretaria_salud"] == "Si":
                    form_fields["parrafo_secretaria_salud"] = "sí"
                    form_fields["acredito"] = "acreditó"

                else:
                    form_fields["parrafo_secretaria_salud"] = "no"
                    if form_fields["acredito"] != "acreditó":
                        form_fields["parrafo_extra_secretaria_salud"] = (
                            PARRAFO_EXTRA_SECRETARIA_SALUD
                        )
                        form_fields["linea_extra_secretaria_salud"] = (
                            LINEA_EXTRA_SECRETARIA_SALUD
                        )
                    else:
                        form_fields["linea_extra_acredito_secretaria_salud"] = (
                            LINEA_EXTRA_ACREDITO_SECRETARIA_SALUD
                        )

        else:
            if form_fields["secretaria_salud"] == "No":
                form_fields["parrafo_secretaria_salud"] = "no"

                if form_fields["acredito"] == "acreditó":
                    form_fields["linea_extra_acredito_secretaria_salud"] = (
                        LINEA_EXTRA_ACREDITO_SECRETARIA_SALUD
                    )
                else:
                    form_fields["parrafo_extra_secretaria_salud"] = (
                        PARRAFO_EXTRA_SECRETARIA_SALUD
                    )
                    form_fields["linea_extra_secretaria_salud"] = (
                        LINEA_EXTRA_SECRETARIA_SALUD
                    )

            else:
                form_fields["parrafo_secretaria_salud"] = "sí"

        return form_fields

    def get_conditional_informacional_laboral(self, form_fields):
        # Se establecen los campos en el form_fields,
        # que corresponden a la seccion informacion laboral.
        # Dias laborables, numero de empleados etc..
        if form_fields["desde_dia"] and form_fields["hasta_dia"]:
            dias_laborables = DIAS_LABORABLES.format(
                desde_dia=form_fields["desde_dia"],
                hasta_dia=form_fields["hasta_dia"],
            )
            form_fields["dias_laborables"] = dias_laborables

        if form_fields["desde_horario"] and form_fields["hasta_horario"]:
            horarios_laborables = HORARIO_LABORABLES.format(
                desde_horario=form_fields["desde_horario"],
                hasta_horario=form_fields["hasta_horario"],
            )
            form_fields["horarios_laborables"] = horarios_laborables

        if form_fields["numero_empleados"]:
            if form_fields["numero_empleados"] == 1:
                numeros_empleados = " y con número total de un empleados (s), "
                form_fields["numeros_empleados"] = numeros_empleados
            else:
                numeros_empleados = NUMEROS_EMPLEADOS.format(
                    numero_empleados=form_fields["numero_empleados"],
                )
                form_fields["numeros_empleados"] = numeros_empleados

        return form_fields

    def get_conditional_individualizacion_sancion(self, form_fields):
        # Se establecen, los campos en el form_fields,
        # que corresponden a la seccion de individualizacion de la
        # sancion.
        lista_cotejo_object = ListaCotejo.objects.get(pk=self.pk)

        if lista_cotejo_object.name == "Covid-19":
            if form_fields["grave"] == "Graves":
                form_fields["grave"] = GRAVE_COVID
            else:
                form_fields["grave"] = NO_GRAVE_COVID
        else:
            if form_fields["grave"] == "Graves":
                form_fields["grave"] = GRAVE
            else:
                form_fields["grave"] = NO_GRAVE

        if form_fields["reincidente"] == "Reincidente":
            form_fields["reincidente"] = REINCIDENTE
        else:
            form_fields["reincidente"] = NO_REINCIDENTE

        return form_fields

    def get_conditional_documentos(self, form_fields):
        # Se establecen las condicionales,
        # para los tipos de documentos seleccionados.
        lista_documentos_presentando = ""
        form_fields["documentos_presentando_merge"] = ""
        documento_notarial = False

        if (
            form_fields["tipo_documento"]
            == "no exhibió documentacion alguna en original o copia certificada que lo acreditara"
        ):
            form_fields["documentos_presentando_merge"] = NO_EXHIBIO_DOCUMENTO

        elif (
            form_fields["tipo_documento"]
            != "no exhibió documentacion alguna en original o copia certificada que lo acreditara"
        ):
            for i in form_fields["presentando"]:
                if i in [
                    "Carta Poder",
                    "Aviso de Funcionamiento de Productos y Servicios",
                ]:
                    lista_documentos_presentando += i + ", "
                elif i == "Otro":
                    lista_documentos_presentando += (
                        form_fields["presentando_otro"] + ", "
                    )
                elif i == "Instrumento Notarial":
                    documento_notarial = True

        if documento_notarial:
            if len(form_fields["presentando"]) == 1:
                documentos_presentando_merge = PARRAFO_INTRUMENTO_NOTORIAL.format(
                    instrumento_numero_notarial=form_fields[
                        "instrumento_numero_notarial"
                    ],
                    dia_notarial=form_fields["dia_notarial"],
                    mes_notarial=form_fields["mes_notarial"],
                    año_notarial=form_fields["año_notarial"],
                    tipo_documento=form_fields["tipo_documento"],
                    licenciado_notarial=form_fields["licenciado_notarial"],
                    notario_publico_nro=form_fields["notario_publico_nro"],
                    del_notarial=form_fields["del_notarial"],
                    personalidad_como=form_fields["aparecen_datos"],
                )
                form_fields["documentos_presentando_merge"] = (
                    documentos_presentando_merge
                )
            else:
                documentos_presentando_merge = (
                    PARRAFO_INTRUMENTO_NOTORIAL_EXTRA_DOCUMENTOS.format(
                        instrumento_numero_notarial=form_fields[
                            "instrumento_numero_notarial"
                        ],
                        dia_notarial=form_fields["dia_notarial"],
                        mes_notarial=form_fields["mes_notarial"],
                        año_notarial=form_fields["año_notarial"],
                        licenciado_notarial=form_fields["licenciado_notarial"],
                        notario_publico_nro=form_fields["notario_publico_nro"],
                        del_notarial=form_fields["del_notarial"],
                        tipo_documento=form_fields["tipo_documento"],
                        lista_documentos_presentando=lista_documentos_presentando,
                        personalidad_como=form_fields["aparecen_datos"],
                    )
                )
                form_fields["documentos_presentando_merge"] = (
                    documentos_presentando_merge
                )
        elif (
            documento_notarial == False
            and form_fields["tipo_documento"]
            != "no exhibió documentacion alguna en original o copia certificada que lo acreditara"
        ):
            documentos_presentando_merge = DOCUMENTO_PRESENTO.format(
                tipo_documento=form_fields["tipo_documento"],
                lista_documentos_presentando=lista_documentos_presentando,
                personalidad_como=form_fields["aparecen_datos"],
            )
            form_fields["documentos_presentando_merge"] = documentos_presentando_merge

        return form_fields

    def get_conditional_parrafo_oir_recibir(self, form_fields, data):
        # Se establecen las condiciones, para crear
        # el field correspondiente para el MergeField
        # `parrafo_oir_recibir`
        parrafo_oir_recibir = ""
        try:
            domicilio_oir = data["domicilio_oir"]
        except:
            domicilio_oir = "off"
        try:
            autorizado_oir = data["autorizados_oir"]
        except:
            autorizado_oir = "off"

        if (
            domicilio_oir == "on"
            and form_fields["domicilio_oir_recibir"]
            and autorizado_oir == "on"
            and form_fields["autorizados_oir_recibir"]
        ):
            parrafo_oir_recibir = DOMICILIO_OIR_RECIBIR_PARRAFO_1.format(
                domicilio_oir_recibir=form_fields["domicilio_oir_recibir"],
                autorizados_oir_recibir=form_fields["autorizados_oir_recibir"],
            )
        elif domicilio_oir == "on" and form_fields["domicilio_oir_recibir"]:
            parrafo_oir_recibir = DOMICILIO_OIR_RECIBIR_PARRAFO_2.format(
                domicilio_oir_recibir=form_fields["domicilio_oir_recibir"],
            )
        elif autorizado_oir == "on" and form_fields["autorizados_oir_recibir"]:
            parrafo_oir_recibir = DOMICILIO_OIR_RECIBIR_PARRAFO_3.format(
                autorizados_oir_recibir=form_fields["autorizados_oir_recibir"],
            )

        form_fields["parrafo_oir_recibir"] = parrafo_oir_recibir

        return form_fields

    def get_conditional_notification_electronica(self, form_fields):
        # Se establecen las condiciones para formar el MergeField,
        # para notificacion electronica.
        if (
            form_fields["notificacion_electronica"] == "si_notificacion_electronica"
            and form_fields["correo_electronico"]
        ):
            form_fields["parrafo_notificacion_electronica"] = (
                PARRAFO_NOTIFICACION_ELECTRONICA.format(
                    correo_electronico=form_fields["correo_electronico"]
                )
            )
            form_fields["leyenda_notificacion_electronica"] = (
                LEYENDA_NOTIFICACION_ELECTRONICA
            )

        return form_fields

    def get_conditional_causas_no_acredito(self, form_fields):
        # Si no se checkado la causa de no acreditar
        # y no se ha ingresado ningun texto,
        # la causa de no acreditar quedará en blanco.
        try:
            if (
                form_fields["no_acredito_cumplimiento"] == "on"
                and form_fields["causa_no_acredito"]
            ):
                form_fields["causa_no_acredito"] = CAUSAS_NO_ACREDITO.format(
                    causa=form_fields["causa_no_acredito"]
                )
        except KeyError:
            # En el caso de que no se haya marcado con check
            # [] Colocar porque no acreditó cumplimiento?
            pass

        return form_fields

    def get_conditional_objeto_alcance(self):
        # Return a dict as a initial for
        # objects and scope (Objeto|Alcance)
        # depending of `Lista cotejo` selected.
        lista_cotejo_object = ListaCotejo.objects.get(pk=self.pk)

        if lista_cotejo_object.name == "Covid-19":
            initial = {"objeto": OBJETO_COVID, "alcance": ALCANCE_COVID}
        elif lista_cotejo_object.name == "Purificadora":
            initial = {"objeto": OBJETO_NORMAL, "alcance": ALCANCE_PURIFICADORAS}
        else:
            initial = {"objeto": OBJETO_NORMAL, "alcance": ALCANCE_NORMAL}

        return initial


@method_decorator(csrf_exempt)
def search_lista(request):
    if request.is_ajax and request.method == "POST":
        data = dict()
        response = json.loads(request.body)
        list_content = ListaCotejo.objects.get(pk=response["id"])
        context = {
            "list_content": list_content,
        }
        data["html_list_cotejo"] = render_to_string("lista/lista_cotejo.html", context)
    return JsonResponse(data)


# @method_decorator(csrf_exempt)
def search_list_versiones(request):
    if request.method == "POST":
        data = list()
        try:
            response = json.loads(request.body)
            list_name = response["list_name"]

            list_cotejo = ListaCotejo.objects.get(name=list_name)
            versiones = list_cotejo.version.all()

            for version in versiones:
                data.append(version.toJSON())
        except Exception as e:
            data = dict()
            data["error"] = str(e)
    return JsonResponse(data, safe=False)


def error_400(request, exception):
    data = {}
    return render(request, "error_pages/400.html", data)


def error_403(request, exception):
    data = {}
    return render(request, "error_pages/403.html", data)


def error_404(request, exception):
    data = {}
    return render(request, "error_pages/404.html", data)


def error_500(request):
    data = {}
    return render(request, "error_pages/500.html", data)
