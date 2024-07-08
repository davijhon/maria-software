lista_fields = ['a', 'b', 'c', 'd']
OPTIONS = ()

for f in lista_fields:
	k = f.capitalize()
	v = f.lower()
	f_tuple = ((k, v))

	OPTIONS += (f_tuple,)




print(OPTIONS)