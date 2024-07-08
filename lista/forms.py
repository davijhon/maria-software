from django import forms

from .models import ListaCotejo, ResolucionBase


OBJETO = 'Reconocimiento sanitario del lugar o actividad que se practica, a fin de constatar el cumplimiento del Segundo Aviso por el que se da conocer el color del Semáforo Epidemiológico de la Ciudad de México y se Establecen Modificaciones al Sexto Acuerdo por el que se Establecen los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México y se crea el Comité de Monitoreo y su Anexo, publicado en la Gaceta Oficial de la Ciudad de México No. 364 Bis del 12 de junio de 2020;  basado en el riesgo epidemiológico y conforme al cual se pondrá en marcha la Nueva Normalidad de manera paulatina y progresiva de las actividades económicas, laborales, sociales, educativas, culturales, de transporte y gubernamentales en la Ciudad de México; así como los específicos para cada sector, establecidas en los avisos, lineamientos,  protocolos, manuales, reglas y/o guías disponibles para su consulta en el enlace electrónico http://covid19.cdmx.gob.mx/medidassanitarias'
ALCANCE = 'Efectuar acciones de vigilancia sanitaria con el propósito de constatar el cumplimiento del Segundo Aviso por el que se da conocer el color del Semáforo Epidemiológico de la Ciudad de México y se Establecen Modificaciones al Sexto Acuerdo por el que se Establecen los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México y se crea el Comité de Monitoreo y su Anexo, clausula Primera, Segunda, Quinta y Sexta publicado en la Gaceta Oficial de la Ciudad de México No. 364 Bis del 12 de junio de 2020; asimismo como el Décimo Tercer Aviso por el que se da a conocer el color del semáforo Epidemiológico de la Ciudad de México y las Medidas de Protección a la Salud que deberán observarse, así como la Modificación a los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México, Clausula Cuarta Décimo Ter, las personas físicas o morales titulares de los establecimientos o responsables de las actividades que conforme al color del Semáforo Epidemiológico se encuentren operando con un plantilla presencial de 100 o más personas por cada centro de trabajo, deberán realizar a su costa y de manera quincenal, pruebas rápidas de antígeno, o bien, en RT-PCR de rección en cadena de la polimerasa detección, para la detección del virus SARS-CoV2, mismas que deberán ser aplicadas en los laboratorios clínicos o lugares autorizados para realizar pruebas COVID-19 en la Ciudad de México, a por lo menos el 10% de la totalidad de dicha plantilla, ya sea en forma individual o grupal,  para el caso de pruebas RT-PCR, publicado en la Gaceta Oficial de la Ciudad de México No. 492Bis del 11 de diciembre de 2020; y establecido en el Trigésimo Séptimo Aviso por el que el Comité de Monitoreo establece medidas extraordinarias de Protección a Salud para disminuir la curva de contagios, derivado de que la Ciudad se encuentra en Semáforo Rojo de Máxima Alerta por la Emergencia de COVID-19, publicado en la Gaceta Oficial de la Ciudad de México No. 498 Bis de 21 de diciembre de 2020 y en los términos previstos en el ordinal Segundo y Quinto en su Nota Aclaratoria publicada en la Gaceta Oficial de la Ciudad de México No. 499 del 22 de diciembre de 2020. Si advierte violaciones a las disposiciones legales de dicho acuerdo, en la necesidad de proteger a la salud a la población, evitar riesgos y daños a la misma que puedan causar con la violación de los preceptos de la Ley General de Salud y la Ley de Salud del Distrito Federal, así como los reglamentos sanitarios y normas oficiales aplicables vigentes, quedara facultado, para ejecutar las medidas de seguridad preventivas a la que se refiere el artículo 404 de la Ley General de Salud, 141 fracción VII, VIII y XIII de la Ley de Salud del Distrito Federal y 26 fracción III del Reglamento de la Agencia de Protección Sanitaria del Gobierno de la Ciudad de México. Para el desarrollo de las actividades, el personal de verificación designado podrá realizar toma fotográfica del establecimiento, de los productos y de las acciones que se realicen en cumplimiento a la presente orden'

DIAS_SEMANA = [
    ('', '------'),
    ('Lunes', 'Lunes'),
    ('Martes', 'Martes'),
    ('Miércoles', 'Miércoles'),
    ('Jueves', 'Jueves'),
    ('Viernes', 'Viernes'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo'),
]

TIPO_ORDEN = [
    ('AGEPSA/CABOSCA/', 'AGEPSA/CABOSCA/'),
    ('CSSCP/', 'CSSCP/'),
]

MODIFICAR_OBJETO = [
    ('Modificar objeto', 'Modificar objeto'),
    ('No modificar objeto', 'No modificar objeto'),
]

MODIFICAR_ALCANCE = [
    ('Modificar alcance', 'Modificar alcance'),
    ('No modificar alcance', 'No modificar alcance'),
]


SECRETARIA_SALUD = [
    ('Si', 'Si'),
    ('No', 'No'),
    ('No requiere', 'No requiere'),
]

MANIFESTACIONES = [
    ('se reservó su derecho a realizar manifestaciones', 'se reservó su derecho a realizar manifestaciones'),
    ('manifestó lo que a su derecho convino', 'manifestó lo que a su derecho convino'),
    ('no realizó manifestaciones', 'no realizó manifestaciones'),
]

TIPO_DOCUMENTO = [
    ('Original', 'Original'),
    ('Copia Simple', 'Copia Simple'),
    ('no exhibió documentacion alguna en original o copia certificada que lo acreditara', 'no exhibió documentacion alguna en original o copia certificada que lo acreditara'),
]

PRESENTANDO = [
    ('Instrumento Notarial', 'Instrumento_Notarial'),
    ('Aviso de Funcionamiento de Productos y Servicios', 'Aviso de Funcionamiento de Productos y Servicios'),
    ('Carta Poder', 'Carta Poder'),
    ('Otro', 'Otro'),
]

PERSONALIDAD = [
    ('Si se reconoce', 'Si se reconoce'),
    ('No se reconoce', 'No se reconoce'),
]

PERSONALIDAD_COMO = [
    ('Propietario', 'Propietario'),
    ('Representante legal', 'Representante legal'),
    ('Representante de los derechos', 'Representante de los derechos'),
    ('Otros', 'Otros'),
]

APARECEN_DATOS = [
    ('PROPIETARIA(O)', 'PROPIETARIA(O)'),
    ('REPRESENTANTE LEGAL', 'REPRESENTANTE LEGAL'),
    ('Otros Datos', 'Otros Datos'),
]


CARTA_COMPROMISO = [
    ('Si Cuenta', 'Si Cuenta'),
    ('No Cuenta', 'No Cuenta'),
]

GRAVE = [
    ('Graves', 'Graves'),
    ('No graves', 'No graves'),
]

ACREDITO = [
    ('acreditó', 'acreditó'),
    ('no acreditó', 'no acreditó'),
]

REINCIDENTE = [
    ('Reincidente', 'Reincidente'),
    ('No Reincidente', 'No Reincidente'),
]

BENEFICIO_ECONOMICO = [
    ('obtuvo un beneficio económico', 'obtuvo un beneficio económico'),
    ('no obtuvo un beneficio económico', 'no obtuvo un beneficio económico'),
]

NOTIFICACION_ELECTRONICA = [
    ('si_notificacion_electronica', 'Si'),
    ('no_notificacion_electronica', 'No'),
]


class ResolutionsForm(forms.Form):
    """
    Representa el formulario para
    la resolucion de la lista de cotejo
    de alimentos. Contiene los campos de los
    tres tipos de actas(Rebeldia, Cumplimiento
    Total, Cumplimiento Parcial)
    """

    # Reporte
    resolucion = forms.ModelChoiceField(queryset=ResolucionBase.objects.order_by('created'), widget=forms.Select(attrs={'class': 'form-control', 'id': 'PlantillaSelect'}))
    fecha_actual = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    expediente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234/2021'}))

    # Direccion Establecimiento
    nombre_establecimiento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mi Establecimiento'}))
    giro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo_postal = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min':'0'}))

    # Datos de Resolucion
    fecha_orden_visita = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    tipo_orden = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPO_ORDEN, required=False)

    numero_orden_verificacion_cabosca = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: VS/EXT/19/1234/2020'}), required=False)
    numero_orden_verificacion_csscp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234/2020'}), required=False)

    modificar_objeto = forms.ChoiceField(widget=forms.RadioSelect, choices=MODIFICAR_OBJETO, required=False)
    objeto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "10"}), required=False)
    
    modificar_alcance = forms.ChoiceField(widget=forms.RadioSelect, choices=MODIFICAR_ALCANCE, required=False)
    alcance = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "10"}), required=False)


    # Considerandos
    fraccion_103 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: XVII'}))
    fraccion_110 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: I, inciso e)'}))
    fraccion_5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: I, inciso i'}))
    fraccion_16 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: I, inciso a)'}),required=False)
    fraccion_17 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: I, inciso h)'}),required=False)


    fecha_practico_visita = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    secretaria_salud = forms.ChoiceField(widget=forms.RadioSelect, choices=SECRETARIA_SALUD, required=False)
    acredito = forms.ChoiceField(widget=forms.RadioSelect, choices=ACREDITO, required=False)
    carta_compromiso = forms.ChoiceField(widget=forms.RadioSelect, choices=CARTA_COMPROMISO, required=False)
    fecha_que_comparece = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    fecha_desde_acude_comparecer = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    fecha_hasta_acude_comparecer = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    recibio_visita = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    puesto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    manifestaciones = forms.ChoiceField(widget=forms.RadioSelect, choices=MANIFESTACIONES, required=False)
    beneficio_economico = forms.ChoiceField(widget=forms.RadioSelect, choices=BENEFICIO_ECONOMICO, required=False)
    
    # Only Parcial | Total
    compareciente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    tipo_de_compareciente = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    tipo_documento = forms.ChoiceField(widget=forms.RadioSelect, choices=TIPO_DOCUMENTO, required=False)

    presentando = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PRESENTANDO, required=False)
    presentando_otro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    # Instrumento Notarial
    instrumento_numero_notarial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    fecha_notarial = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    licenciado_notarial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    notario_publico_nro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    del_notarial = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial='Distrito Federal, ahora Ciudad de Mexico', required=False)

    # personalidad = forms.ChoiceField(widget=forms.RadioSelect, choices=PERSONALIDAD, required=False)
    personalidad_otro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    personalidad_como = forms.ChoiceField(widget=forms.RadioSelect, choices=PERSONALIDAD_COMO, required=False)
    personalidad_como_otro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    aparecen_datos = forms.ChoiceField(widget=forms.RadioSelect, choices=APARECEN_DATOS, required=False)
    aparecen_datos_otro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    domicilio_oir_recibir = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Anote direccion con codigo postal'}), required=False)
    autorizados_oir_recibir = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres Completos'}), required=False)

    causa_no_acredito = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "2"}), required=False)
    folio_carta_compromiso = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    # Individualizacion de la sancion
    grave =  forms.ChoiceField(widget=forms.RadioSelect, choices=GRAVE,  required=False)
    desde_dia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=DIAS_SEMANA, required=False)
    hasta_dia = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=DIAS_SEMANA, required=False)
    desde_horario = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'time'}), required=False)
    hasta_horario = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'time'}), required=False)
    numero_empleados = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min':'0'}), required=False)
    reincidente =  forms.ChoiceField(widget=forms.RadioSelect, choices=REINCIDENTE, required=False)
    aprobador = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial='JULIO ALEJANDRO PACHECO GRANADOS')
    iniciales = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    notificacion_electronica = forms.ChoiceField(widget=forms.RadioSelect, choices=NOTIFICACION_ELECTRONICA, required=False)
    correo_electronico = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)