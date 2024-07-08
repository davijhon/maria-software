# This are the constant that are used to
# generated single or compounds paragraphs.
#
# The single paragraphs, are a line of
# information.
#
# Compounds paragraphs, are a line of 
# information with elements {}, to
# sustited with one o multiple information.

# List of available fields
FIELDS = [
	'resolucion', 'fecha', 'expediente', 'nombre_establecimiento',
	'giro', 'direccion', 'codigo_postal', 'fecha_orden_visita',
	'objeto', 'alcance', 'diligencia_que', 'secretaria_salud', 
	'comparecieron', 'numero_orden_verificacion', 'compareciente', 'tipo_de_compareciente',
	'recibio_visita', 'puesto',  'desde_dia', 
	'hasta_dia', 'desde_horario', 'hasta_horario', 'numero_empleados', 
	'fecha_acude_comparecer', 'aprobador', 'iniciales', 'name', 
	'csrfmiddlewaretoken', 'fracciones1', 'fracciones2', 
	'fracciones3', 'hasta_acude_comparecer', 'numerales_contravenidos', 'finalidad', 
	'cumplimiento', 'anexo', 'lista_cotejo_name', 'nom_fundamento', 
	'fraciones_incisos', 'grave', 'reincidente', 'folio', 'carta_compromiso',
	'manifestaciones', 'presentando', 'personalidad', 'personalidad_como',
	'domicilio_oir_recibir', 'causa_no_acredito', 'folio_carta_compromiso',
	'no_acredito_cumplimiento',
]



OBJETO_COVID = 'Reconocimiento sanitario del lugar o actividad que se practica, a fin de constatar el cumplimiento del Segundo Aviso por el que se da conocer el color del Semáforo Epidemiológico de la Ciudad de México y se Establecen Modificaciones al Sexto Acuerdo por el que se Establecen los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México y se crea el Comité de Monitoreo y su Anexo, publicado en la Gaceta Oficial de la Ciudad de México No. 364 Bis del 12 de junio de 2020;  basado en el riesgo epidemiológico y conforme al cual se pondrá en marcha la Nueva Normalidad de manera paulatina y progresiva de las actividades económicas, laborales, sociales, educativas, culturales, de transporte y gubernamentales en la Ciudad de México; así como los específicos para cada sector, establecidas en los avisos, lineamientos,  protocolos, manuales, reglas y/o guías disponibles para su consulta en el enlace electrónico http://covid19.cdmx.gob.mx/medidassanitarias'
ALCANCE_COVID = 'Efectuar acciones de vigilancia sanitaria con el propósito de constatar el cumplimiento del Segundo Aviso por el que se da conocer el color del Semáforo Epidemiológico de la Ciudad de México y se Establecen Modificaciones al Sexto Acuerdo por el que se Establecen los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México y se crea el Comité de Monitoreo y su Anexo, clausula Primera, Segunda, Quinta y Sexta publicado en la Gaceta Oficial de la Ciudad de México No. 364 Bis del 12 de junio de 2020; asimismo como el Décimo Tercer Aviso por el que se da a conocer el color del semáforo Epidemiológico de la Ciudad de México y las Medidas de Protección a la Salud que deberán observarse, así como la Modificación a los Lineamientos para la Ejecución del Plan Gradual hacia la Nueva Normalidad en la Ciudad de México, Clausula Cuarta Décimo Ter, las personas físicas o morales titulares de los establecimientos o responsables de las actividades que conforme al color del Semáforo Epidemiológico se encuentren operando con un plantilla presencial de 100 o más personas por cada centro de trabajo, deberán realizar a su costa y de manera quincenal, pruebas rápidas de antígeno, o bien, en RT-PCR de rección en cadena de la polimerasa detección, para la detección del virus SARS-CoV2, mismas que deberán ser aplicadas en los laboratorios clínicos o lugares autorizados para realizar pruebas COVID-19 en la Ciudad de México, a por lo menos el 10% de la totalidad de dicha plantilla, ya sea en forma individual o grupal,  para el caso de pruebas RT-PCR, publicado en la Gaceta Oficial de la Ciudad de México No. 492Bis del 11 de diciembre de 2020; y establecido en el Trigésimo Séptimo Aviso por el que el Comité de Monitoreo establece medidas extraordinarias de Protección a Salud para disminuir la curva de contagios, derivado de que la Ciudad se encuentra en Semáforo Rojo de Máxima Alerta por la Emergencia de COVID-19, publicado en la Gaceta Oficial de la Ciudad de México No. 498 Bis de 21 de diciembre de 2020 y en los términos previstos en el ordinal Segundo y Quinto en su Nota Aclaratoria publicada en la Gaceta Oficial de la Ciudad de México No. 499 del 22 de diciembre de 2020. Si advierte violaciones a las disposiciones legales de dicho acuerdo, en la necesidad de proteger a la salud a la población, evitar riesgos y daños a la misma que puedan causar con la violación de los preceptos de la Ley General de Salud y la Ley de Salud del Distrito Federal, así como los reglamentos sanitarios y normas oficiales aplicables vigentes, quedara facultado, para ejecutar las medidas de seguridad preventivas a la que se refiere el artículo 404 de la Ley General de Salud, 141 fracción VII, VIII y XIII de la Ley de Salud del Distrito Federal y 26 fracción III del Reglamento de la Agencia de Protección Sanitaria del Gobierno de la Ciudad de México. Para el desarrollo de las actividades, el personal de verificación designado podrá realizar toma fotográfica del establecimiento, de los productos y de las acciones que se realicen en cumplimiento a la presente orden'

OBJETO_NORMAL = 'Reconocimiento sanitario del lugar o actividad que se practica, a fin de evaluar las condiciones sanitarias y el cumplimiento de las disposiciones en la materia contenidas en la Ley General de Salud, referente al Artículo 200 bis, la Ley de Salud del Distrito Federal, sus reglamentos y conforme a la Norma Oficial Mexicana NOM-251-SSA1-2009, Prácticas de Higiene para el Proceso de Alimentos, Bebidas o Suplementos Alimenticios, y demás disposiciones normativas aplicables'
ALCANCE_NORMAL = 'Efectuar acciones de verificación de las condiciones sanitarias del establecimiento, orientación y educación sobre actos u omisiones a las disposiciones sanitarias vigentes. Si advierte violaciones a las disposiciones legales, detecta expendio y/o exhibición de productos ajenos a la actividad propia del giro, en la necesidad de proteger a la salud a la población, evitar peligros y daños a la misma que puedan causar con la violación de los preceptos de la Ley General de Salud y la Ley de Salud del Distrito Federal, así como los Reglamentos Sanitarios y normas oficiales aplicables vigentes, quedará facultado, para ejecutar las medidas de seguridad preventivas a las que se refiere el artículo 397 de la Ley General de Salud, 141 fracción VII, VIII y XIII de la Ley de Salud del Distrito Federal y 26 fracción VII del Reglamento de la Agencia de Protección Sanitaria del Gobierno de la Ciudad de México, para el desarrollo de las actividades, el personal de verificación designado podrá realizar toma fotográfica del establecimiento, de los productos y de las acciones que se realicen en cumplimiento a la presente orden'

ALCANCE_PURIFICADORAS = 'Efectuar acciones de verificación de las condiciones sanitarias del establecimiento, orientación y educación sobre actos u omisiones a las disposiciones sanitarias vigentes. Si advierte violaciones a las disposiciones legales, detecta expendio y/o exhibición de productos ajenos a la actividad propia del giro, en la necesidad de proteger a la salud a la población, evitar peligros y daños a la misma que puedan causar con la violación de los preceptos de la Ley General de Salud y la Ley de Salud del Distrito Federal, así como los Reglamentos Sanitarios y normas oficiales aplicables vigentes, quedará facultado, para ejecutar las medidas de seguridad preventivas a las que se refiere el artículo 397 de la Ley General de Salud, 141 fracción VII, VIII y XIII de la Ley de Salud del Distrito Federal y 26 fracción VII del Reglamento de la Agencia de Protección Sanitaria del Gobierno de la Ciudad de México'

GRAVE_COVID = 'es considerado grave, pues generó un riesgo sanitario a la población al realizar su actividad sin dar cumplimiento a los Acuerdos referidos en el párrafo anterior, que tiene la finalidad de prever y evitar la propagación del COVID-19.'
NO_GRAVE_COVID = 'es considerado como no grave, pues no generó un riesgo sanitario a la población al realizar su actividad sin dar cumplimiento a los Acuerdos referidos en el párrafo anterior, que tiene la finalidad de prever y evitar la propagación del COVID-19.'
PARRAFO_ES_GRAVE = 'pues generó un riesgo sanitario a la población al realizar su actividad sin dar cumplimiento a los Acuerdos referidos en el párrafo anterior, que tiene la finalidad de prever y evitar la propagación del COVID-19.'

GRAVE = 'grave, pues generó'
NO_GRAVE = 'no grave, pues no generó'

REINCIDENTE = 'se configura'
NO_REINCIDENTE = 'no se configura'

PARRAFO_SECRETARIA_SALUD = 'Asimismo, se asentó en el apartado denominado Información Administrativa que {secretaria_salud} cuenta con el Aviso de Funcionamiento ante la Secretaría de Salud.'
PARRAFO_EXTRA_SECRETARIA_SALUD = 'Asimismo, se advierte que en el apartado denominado INFORMACIÓN ADMINISTRATIVA del Acta de Verificación que nos ocupa, fue señalado que no cuenta con el Aviso de Funcionamiento ante la Secretaría de salud, aviso que es obligatorio en términos del artículo 200 Bis de la Ley General de salud, por lo que, deberá tramitarlo en el Centro Integral de Servicios de la Agencia de Protección Sanitaria del Gobierno de la Cuidad de México, ubicado en Torre Insignia, Avenida Insurgentes Norte, número 423, Colonia San Simón Tolnahuac, Alcaldía Cuauhtémoc, C.P. 06900, Ciudad de México.'
LINEA_EXTRA_SECRETARIA_SALUD = 'así como deberá tener exhibido en lugar visible su Aviso de Funcionamiento,'
LINEA_EXTRA_ACREDITO_SECRETARIA_SALUD = 'Asimismo, acreditó contar con su respectivo Aviso de Funcionamiento ante Secretaría de Salud.'

DOCUMENTO_PRESENTO = 'ya que solo presentó {tipo_documento} de {lista_documentos_presentando} donde aparecen sus datos como "{personalidad_como}" del establecimiento visitado, '
NO_EXHIBIO_DOCUMENTO = 'no exhibío documentacion alguna en original o copia certificada que la acreditara,'
PARRAFO_INTRUMENTO_NOTORIAL = 'ya que solo presentó {tipo_documento} de Instrumento Notorial número {instrumento_numero_notarial} de fecha {dia_notarial} de {mes_notarial} del {año_notarial}, pasado ante la fe del Licendiado {licenciado_notarial}, Notario Público No. {notario_publico_nro} del {del_notarial}, donde aparecen sus datos como {personalidad_como} del establecimiento visitado, '
PARRAFO_INTRUMENTO_NOTORIAL_EXTRA_DOCUMENTOS = 'ya que solo presentó {tipo_documento} de Instrumento Notorial número {instrumento_numero_notarial} de fecha {dia_notarial} de {mes_notarial} del {año_notarial}, pasado ante la fe del Licendiado {licenciado_notarial}, Notario Público No. {notario_publico_nro} del {del_notarial}, y {tipo_documento} de {lista_documentos_presentando} donde aparecen sus datos como "{personalidad_como}" del establecimiento visitado, '

DOMICILIO_OIR_RECIBIR_PARRAFO_1 = 'Con base en lo manifestado, se tiene por señalado como domicilio para oír y recibir notificaciones el ubicado en {domicilio_oir_recibir}, en la Ciudad de México. Así como por autorizados para los mismos efectos al (los) CC. {autorizados_oir_recibir}.'
DOMICILIO_OIR_RECIBIR_PARRAFO_2 = 'Con base en lo manifestado, se tiene por señalado como domicilio para oír y recibir notificaciones el ubicado en {domicilio_oir_recibir}, en la Ciudad de México.'
DOMICILIO_OIR_RECIBIR_PARRAFO_3 = 'Téngase por autorizado al (os, as) C (CC). {autorizados_oir_recibir} en términos del articulo42 de la Ley de procedimiento Administrativo de la Ciudad de México.'

DIAS_LABORABLES = 'con días laborables: {desde_dia} a {hasta_dia};'
HORARIO_LABORABLES = 'con horario de labores de {desde_horario} a {hasta_horario} horas;'
NUMEROS_EMPLEADOS = 'número total de {numero_empleados} empleado (s), '

LINEA_CSSCP = 'Coordinación de Servicios de Salud y de Cuidados Personales'
LINEA_CABOSCA = 'Coordinación de Alimentos, Bebidas, Otros Servicios y Control Analítico'

PARRAFO_NOTIFICACION_ELECTRONICA = 'Asimismo, del análisis de las constancias que integran el presente expediente se advierte que, el compareciente manifestó su autorización para que las notificaciones que deban realizarse en el presente procedimiento aun las que se estimen de carácter personal, le sean notificadas al correo electrónico {correo_electronico}'
LEYENDA_NOTIFICACION_ELECTRONICA = 'Este documento ha sido firmado mediante el uso de la FIRMA ELECTRÓNICA DE LA CIUDAD DE MÉXICO (FIRMA CDMX) a cargo del servidor público Mtro. Julio Alejandro Pacheco Granados, Coordinador de Evaluación Técnico Normativa de la Agencia de Protección Sanitaria del Gobierno de la Ciudad de México, amparada a través del Certificado Electrónico al que se refieren los artículos 2, fracción VII y 43 de la Ley de Ciudadanía Digital de la Ciudad de México. Lo anterior, tiene su fundamento en el artículo 6 fracciones XXV y XXVI de la Ley de Operación e Innovación Digital para la Ciudad de México; los Lineamientos que deberán observarse en la Implementación y Uso de la Firma CDMX para las personas servidoras públicas de la Administración Pública de la Ciudad de México; la Política de Gobierno Digital de la Ciudad de México.  Asimismo, de conformidad con lo dispuesto en los artículos 11 fracción VII, 42 fracción II de la Ley de Operación e Innovación Digital para la Ciudad de México y 6 fracción VI de la Ley de Procedimiento Administrativo de la Ciudad de México, la Firma-CDMX tendrá la misma validez jurídica que la firma autógrafa.  Para verificar el certificado digital de la FIRMA CDMX, podrá:  1.- Abrir el oficio (archivo pdf) mediante la aplicación diseñada para ello, para lo cual podrá descargar la aplicación mediante el siguiente enlace: https://drive.google.com/file/d/1Lkue5drw_rQSBN-Th_w2lYovzA6ZTwdz/view?usp=sharing, una vez instalada, ingresar mediante su cuenta Llave CDMX, (si aún no tiene cuenta, la puede obtener ingresando a https://llave.cdmx.gob.mx). 2.- Abrir el oficio (archivo PDF) utilizando Adobe Acrobat. Una vez abierto, se deberá dar clic en el logo que se encuentra en la parte inferior al centro para conocer los datos del firmante.'

CAUSAS_NO_ACREDITO = 'toda vez que: {causa};'