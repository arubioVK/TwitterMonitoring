
import datetime
from dateutil.parser import parse
from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import Info_Twitter, Tweet_History
from app.extras.patrones import expubicacionactive, expidiomaactive, exppatronhora
from app.extras.monitoring import loginTweet, obtenerIDtwitter, matarStream, backgroundstream

def find_or_create_InfoTwitter (idd, user_id, request):
    lerrores = []
    usuario_twitter = request.form['nombre_twitter']
    auth =  loginTweet(request.form['consumer_key'], request.form['consumer_secret'], request.form['access_token'], request.form['access_token_secret'])
    (clavescorrectas, iduser_twitter)=obtenerIDtwitter(auth, usuario_twitter)
    if not(clavescorrectas):
	lerrores.append('Claves o Usuario incorrectos')
#ComprobarParametros Correctos
    try:
	enlaces_active=bool(request.form['enlaces_active'])
    except:
	enlaces_active=False	
    try:
	palabrotas_active=bool(request.form['palabrotas_active'])
    except:
	palabrotas_active=False
    try:
	streamer_active =bool(request.form['streamer_active'])
    except:
	streamer_active =False
    try:
	borrar_active =bool(request.form['borrar_active'])
    except:
	borrar_active =False

    restriccion_hora_min=request.form['restriccion_hora_min']
    restriccion_hora_max=request.form['restriccion_hora_max'] 

    if (restriccion_hora_min =='' and restriccion_hora_max != '') or (restriccion_hora_min !=''and restriccion_hora_max== '' ):
	lerrores.append('Ambas horas tienen que tener valor o ninguna de ellas debe tenerlo')
    elif (restriccion_hora_min !='' and restriccion_hora_max !=''):
	if( not(exppatronhora(restriccion_hora_min))):
	    lerrores.append('La hora inicio no cumple el patron HH:MM')
	elif( not(exppatronhora(restriccion_hora_max))):
	    lerrores.append('La hora fin no cumple el patron HH:MM')
	else:
	    restriccion_hora_min = parse(restriccion_hora_min)
	    restriccion_hora_max = parse(restriccion_hora_max)
	    if(restriccion_hora_min>restriccion_hora_max):
	        lerrores.append('La hora de inicio tiene que ser menor que la hora de finalizacion')
    else:
	restriccion_hora_min = None
        restriccion_hora_max = None

    idioma_active = request.form['idioma_active']
    if(idioma_active!='')and not(expidiomaactive(idioma_active)):
	lerrores.append('No puede tener ese valor idioma')
    elif idioma_active == '':
	idioma_active = None


    ubicacion_active = request.form['ubicacion_active']
    if(ubicacion_active!='')and not(expubicacionactive(ubicacion_active)):
	lerrores.append('No puede tener ese valor de Ubicacion')
    elif ubicacion_active =='':
	ubicacion_active = None

    if lerrores !=[]:
	return lerrores   

    if idd==0:
	#CREAR
	Info_Twitters = Info_Twitter(user_id = user_id,
			       usuario_twitter = usuario_twitter,
                    	       iduser_twitter= iduser_twitter,
                               consumer_key =request.form['consumer_key'],
                               consumer_secret = request.form['consumer_secret'],
                               access_token = request.form['access_token'],
                               access_token_secret = request.form['access_token_secret'],
			       enlaces_active=enlaces_active,
			       idioma_active=idioma_active,
			       palabrotas_active=palabrotas_active,
			       restriccion_hora_min=restriccion_hora_min,
			       restriccion_hora_max=restriccion_hora_max,
			       ubicacion_active =ubicacion_active,
			       streamer_active = streamer_active,
			       borrar_active = borrar_active)
	matar_proceso = False
    else:
	Info_Twitters = Info_Twitter.query.filter(Info_Twitter.id ==idd).filter(Info_Twitter.user_id ==user_id).first()
	#UPDATE
	matar_proceso = Info_Twitters.streamer_active
	Info_Twitters.user_id=user_id
	Info_Twitters.usuario_twitter = usuario_twitter
	Info_Twitters.iduser_twitter=iduser_twitter
	Info_Twitters.consumer_key=request.form['consumer_key']
	Info_Twitters.consumer_secret=request.form['consumer_secret']
	Info_Twitters.access_token = request.form['access_token']
	Info_Twitters.access_token_secret =request.form['access_token_secret'] 
	Info_Twitters.enlaces_active = enlaces_active
	Info_Twitters.idioma_active= idioma_active
	Info_Twitters.palabrotas_active = palabrotas_active
	Info_Twitters.restriccion_hora_min = restriccion_hora_min
	Info_Twitters.restriccion_hora_max = restriccion_hora_max
	Info_Twitters.ubicacion_active =ubicacion_active
	Info_Twitters.streamer_active = streamer_active
	Info_Twitters.borrar_active = borrar_active

    # Save to DB
    db.session.add(Info_Twitters)
    db.session.commit()
    if matar_proceso:
    #MATAR STREAM ANTERIOR DE ESA CUENTA
	print('Matamos el Streamer que estaba antes')
	matarStream(Info_Twitters.id)
    #LEVANTAR SERVICIO
    if streamer_active:
        print('Levantamos nuevo Streamer')
	print(Info_Twitters.id)
        t1=backgroundstream(auth, iduser_twitter, Info_Twitters.id ,user_id )
        t1.start()
    return lerrores


