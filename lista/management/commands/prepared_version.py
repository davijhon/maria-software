# Modulo para preparar 
# cada Punto de una lista de cotejo
# y asignarle una version, segun la 
# relacion existente con su lista de cotejo.
#
# Nota: La Version de Covid no se toma, ya que contiene
# 3 tipos de versiones. ( Se le hará un tratado especial aparte)
#
# E.g:
#
# Punto1, Alimentos ---- (Se le asigna una version)--> Version 1, Alimentos.

from lista.models import Version, PuntosListaCotejo
from django.core.management.base import BaseCommand


class Command(BaseCommand):


   def handle(self, *args, **options):
      version_list = versions = Version.objects.exclude(lista_cotejo__name='Covid-19')

      lista_cotejo_name_in_version = [version.lista_cotejo for version in version_list]
      puntos_lista_cotejo = PuntosListaCotejo.objects.exclude(lista_cotejo__name='Covid-19')

      for punto in puntos_lista_cotejo:
         if punto.lista_cotejo in lista_cotejo_name_in_version:
            version = version_list.get(lista_cotejo__id=punto.lista_cotejo.id)
            punto.version = version
            punto.save()
      
      print('Done!')
