from django.contrib import admin

from .models import (
    ListaCotejo,
    PuntosListaCotejo,
    ResolucionBase,
    PlantillasBases,
    Version,
)


class VersionAdmin(admin.ModelAdmin):
    fields = (
        "nombre_version",
        "comentario",
        "lista_cotejo",
    )


class PuntoListaAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "numero_punto",
        "punto_acta",
        "lista_cotejo",
        "version",
    ]
    search_fields = ["numero_punto"]
    list_editable = ["numero_punto"]
    list_filter = ["lista_cotejo", "numero_punto", "version"]
    fields = (
        "numero_punto",
        "lista_cotejo",
        "version",
        "punto_acta",
        "fundamento_legal",
        "como_subsanar",
    )


admin.site.register(PuntosListaCotejo, PuntoListaAdmin)


class PlantillasBasesAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "lista_cotejo",
        "created",
    ]
    list_filter = ["lista_cotejo"]


admin.site.register(PlantillasBases, PlantillasBasesAdmin)


admin.site.register(Version, VersionAdmin)
admin.site.register(ListaCotejo)
admin.site.register(ResolucionBase)
