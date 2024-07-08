from django.db import models
from django.template.defaultfilters import slugify
# from smart_selects.db_fields import ChainedForeignKey



class ListaCotejo(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Lista de Cotejo'
        verbose_name_plural = 'Listas de Cotejos'
        ordering = ['id']

    def __str__(self):
        return self.name


class Version(models.Model):
    """
        La version que puede tener una lista de cotejo.

        Una lista de cotejo, puede tener diferentes tipos de versiones.
        Cada version representará una opcion a seleccionar, para poder
        escoger la redaccion y contenido de una Plantilla Base.
    """
    nombre_version = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True, unique=True)
    comentario = models.CharField(max_length=40, help_text="Un pequeño comentario para especificar las caracteristicas de la version.")
    created = models.DateTimeField(auto_now_add=True)
    lista_cotejo = models.ForeignKey(ListaCotejo, on_delete=models.CASCADE, blank=True, null=True, related_name='version')


    def __str__(self):
        return self.nombre_version


    def toJSON(self):
        item = dict()
        item['id'] = self.id
        item['nombre_version'] = self.nombre_version
        item['comentario'] = self.comentario
        item['id_lista_cotejo'] = self.lista_cotejo.id
        item['slug'] = self.slug

        return item

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre_version)
        return super().save(*args, **kwargs)


class PuntosListaCotejo(models.Model):
    numero_punto = models.IntegerField()
    lista_cotejo = models.ForeignKey(ListaCotejo, on_delete=models.CASCADE)
    punto_acta = models.TextField()
    fundamento_legal = models.TextField(null=True, blank=True)
    como_subsanar = models.TextField(null=True, blank=True)
    cumple = models.IntegerField(default=0)
    no_cumple = models.IntegerField(default=1)
    n_a =models.IntegerField(default=2)
    version = models.BooleanField(default=None)
    # version = ChainedForeignKey(
    #     Version,
    #     chained_field="lista_cotejo",
    #     chained_model_field="lista_cotejo",
    #     show_all=False,
    #     auto_choose=True,
    #     sort=True,
    #     blank=True,
    #     null=True,
    # )

    class Meta:
        verbose_name = 'Punto de Lista de Cotejo'
        verbose_name_plural = 'Puntos de Listas de Cotejos'
        ordering = ['id']
            
    def __str__(self):
        return 'Punto {}, de lista {}'.format(self.numero_punto, self.lista_cotejo)


class ResolucionBase(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['created']


    def __str__(self):
        return self.name


def upload_to(instance, filename):
    # Upload  `Plantilla Base`
    # in a file tree like
    # this:
    # Plantillas Bases:
#       - <nombre_lista_de_cotejo>
            # - Rebeldia
            # - Cumplimiento Parcial
            # - Cumplimiento Total

#       - <otra_lista_de_cotejo>
#       ......................
    return '{}/{}.docx'.format(instance.lista_cotejo.name, instance.type_resolution.name)
class PlantillasBases(models.Model):
    type_resolution = models.ForeignKey(ResolucionBase, on_delete=models.CASCADE)
    lista_cotejo = models.ForeignKey(ListaCotejo, on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, upload_to=upload_to)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    
    class Meta:
        verbose_name = 'Plantilla Base'
        verbose_name_plural = 'Plantillas Bases'
        ordering = ['created']

    
    def __str__(self):
        return self.type_resolution.name