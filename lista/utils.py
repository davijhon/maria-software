import pprint
import datetime
from num2words import num2words
from .models import PuntosListaCotejo
from .constants import FIELDS

MESES = {
    "01":'Enero',
    "02":'Febrero',
    "03":'Marzo',
    "04":'Abril',
    "05":'Mayo',
    "06":'Junio',
    "07":'Julio',
    "08":'Agosto',
    "09":'Septiembre',
    "10":'Octubre',
    "11":'Noviembre',
    "12":'Diciembre'
}

def date2words(date):
   # Recibe una <class 'datetime.datetime'> y
   # Devuelve una tupla de 3 valores. Que corresponden a  dia, año, mes 
   # Transforma el <class 'datetime.datetime'> a -> Palabras
   # Ej: 27/3/2021 -> veintisiete, Marzo, dos mil veintiuno
   tuple_dias = ()
   try:
      dia_año = str(date.strftime("%d/%Y")).split('/')
      mes_date = str(date.strftime("%m"))

      for num in dia_año:
         num_in_word = num2words(num, lang='es') # Transforma el num a palabra en lenguaje español
         if num_in_word == 'uno':
            num_in_word = 'un'
         tuple_dias += (num_in_word,)
      
      tuple_dias += (MESES[mes_date],)
   except:
      tuple_dias = ('', '', '',) 

   return tuple_dias

def listado_cumple_no_cumple(lista):
   # Convierte una lista en un string.
   #E.j: ['1', '2', '3'] -> '1, 2 y 3, '
   new_list = list()
   for j in lista:
      obj = PuntosListaCotejo.objects.get(id=j)
      new_list.append(obj.numero_punto)

   new_string = ''
   for i in range(0, len(new_list)):
      if i != len(new_list) - 2:
         new_string += str(new_list[i]) + ', '
      else:
         new_string += str(new_list[i]) + ' y '
   return new_string

def make_list_pts_cotejo(list_fields):
   # Genere tres lista de tuplas
   # de todo el checklist.
   # Se filtran todos los
   # campos, que no esten en
   # `fields`.
	checklist_list = list()
	puntos_cumple_no_cumple = list()
	puntos_no_cumple = list()
	puntos_cumple = list()
	
	for field in list_fields:
		if field[0] not in FIELDS:
			checklist_list.append(field)
	
	# Se dividen los puntos que no cumple y los puntos que cumplen
	for i in checklist_list:
		if i[1] == '1' or i[1] == '0':
			puntos_cumple_no_cumple.append(i[0])
		if i[1] == '1':
			puntos_no_cumple.append(i[0])
		elif i[1] == '0':
			puntos_cumple.append(i[0])
	
	return puntos_cumple_no_cumple, puntos_no_cumple, puntos_cumple


def json_deserializer(in_dict):
  # Procesa un json, que provenga del request de ajax,
  # con el siguiente formato: {'Objecto1': [{'name': Name0,'value': Value0}]}
  # creando nuevos diccionarios, unicamente con keys y values. Limpiando
  # los keys('name'), y los values('value'), procedentes de Jquery/JavaScript.
   out_dict = {}
   for i in range(0, len(in_dict)):
      k = in_dict[i]['name']
      v = in_dict[i]['value']

      # Because `presentando` need to be a list of options.
      if k == 'presentando':
        if 'presentando' in out_dict.keys():
          out_dict['presentando'].append(v)
        else:
          lista = [v]
          out_dict[k] = lista
      else:
        out_dict[k] = v

   return out_dict
