
import datetime
from dateutil.parser import parse
from app import db
from app.extras.patrones import exppatronurls, exppatronpalabrotas
from app.models.user_models import Info_Twitter, Tweet_History


def calificar_enlaces(lurls):
    for url in lurls:
	url_completa=url.get('expanded_url')
	if (exppatronurls(url_completa)):
		return False
    return True

def calificar_idioma(idioma_user, idioma_tweet):
    if idioma_tweet is None:
	return None
    return idioma_user==idioma_tweet


def calificacion_palabrotas(texto_tweet):
    return not(exppatronpalabrotas(texto_tweet))


def calificacion_hora(hora_inicio, hora_fin, hora_tweet):
    hora_inicio = parse(hora_inicio)
    hora_fin = parse(hora_fin)
    return hora_inicio.time()<=hora_tweet.time() and hora_tweet.time()<=hora_fin.time()

def calificacion_ubicacion(ubicacion_user, ubicacion_tweet):
    if ubicacion_tweet is None:
	return None
    return ubicacion_user==ubicacion_tweet.get('country_code')

def calificar_almacenar_rt(idd, user_id, tweet, engine):
    Info_Twitters = engine.execute('SELECT * FROM info_twitter where id=:idd and user_id=:user_id', idd=idd, user_id=user_id).first()
#Extraemos Info Necesaria del Tweet
    tweet_id = tweet.get('id')
    if (tweet.get('retweeted_status').get('extended_tweet') is not None):
	texto_tweet=tweet.get('retweeted_status').get('extended_tweet').get('full_text')
	lurls = tweet.get('retweeted_status').get('extended_tweet').get('entities').get('urls')
    else:
	texto_tweet=tweet.get('retweeted_status').get('text')
	lurls = tweet.get('retweeted_status').get('entities').get('urls')
    created_at = parse(tweet.get('created_at'))
    ubicacion = tweet.get('place')
    autor = tweet.get('retweeted_status').get('user').get('screen_name')
    lang = tweet.get('retweeted_status').get('lang')
#Calificamos el cumplimiento de los diversos campos
#Calificacion las urls
    if Info_Twitters.enlaces_active:
	bcalificacion_enlaces = calificar_enlaces(lurls)
    else:
	bcalificacion_enlaces = None
	#Calificacion del idioma
    if Info_Twitters.idioma_active is not None:
	bcalificacion_idioma = calificar_idioma(Info_Twitters.idioma_active, lang)
    else:
	bcalificacion_idioma = None

	#Calificacion de las palabrotas
    if Info_Twitters.palabrotas_active:
	bcalificacion_palabrotas = calificacion_palabrotas(texto_tweet)
    else:
	bcalificacion_palabrotas = None

	#Calificacion la hora
    if Info_Twitters.restriccion_hora_min is not None:
	bcalificacion_hora = calificacion_hora(Info_Twitters.restriccion_hora_min, Info_Twitters.restriccion_hora_max, created_at)	
    else:
	bcalificacion_hora = None

	#Calificacion la ubicacion
    if Info_Twitters.ubicacion_active is not None:
	bcalificacion_ubicacion = calificacion_ubicacion(Info_Twitters.ubicacion_active, ubicacion)
    else:
	bcalificacion_ubicacion = None
    pasaFiltro = 2
	#No pasa el filtro
    if((bcalificacion_enlaces is not None)and(not(bcalificacion_enlaces))) or ((bcalificacion_idioma is not None)and(not(bcalificacion_idioma))) or ((bcalificacion_palabrotas is not None)and(not(bcalificacion_palabrotas)))or((bcalificacion_hora is not None)and(not(bcalificacion_hora)))or((bcalificacion_ubicacion is not None)and(not(bcalificacion_ubicacion))):
	if (Info_Twitters.borrar_active):
		pasaFiltro = 0
	else:
		pasaFiltro = 1
    engine.execute('INSERT INTO tweet_history (user_id, tweet_id, texto_tweet, autor_tweet, calificacion_enlaces, calificacion_idioma, calificacion_palabrotas, calificacion_hora, calificacion_ubicacion, created_at) VALUES (:user_id, :tweet_id, :texto_tweet, :autor, :bcalificacion_enlaces, :bcalificacion_idioma, :bcalificacion_palabrotas, :bcalificacion_hora, :bcalificacion_ubicacion, :created_at)', user_id=user_id, tweet_id=tweet_id, texto_tweet=texto_tweet, autor=autor, bcalificacion_enlaces=bcalificacion_enlaces, bcalificacion_idioma=bcalificacion_idioma, bcalificacion_palabrotas=bcalificacion_palabrotas, bcalificacion_hora=bcalificacion_hora, bcalificacion_ubicacion=bcalificacion_ubicacion, created_at=created_at)
    return pasaFiltro




def calificar_almacenar_tweet(idd, user_id, tweet, engine):
    Info_Twitters = engine.execute('SELECT * FROM info_twitter where id=:idd and user_id=:user_id', idd=idd, user_id=user_id).first()
#Extraemos Info Necesaria del Tweet
    tweet_id = tweet.get('id')
    if (tweet.get('extended_tweet') is not None):
	texto_tweet=tweet.get('extended_tweet').get('full_text')
	lurls = tweet.get('extended_tweet').get('entities').get('urls')
    else:
	texto_tweet=tweet.get('text')
	lurls = tweet.get('entities').get('urls')
    created_at = parse(tweet.get('created_at'))
    ubicacion = tweet.get('place')
    autor = tweet.get('user').get('screen_name')
    lang = tweet.get('lang')
#Calificamos el cumplimiento de los diversos campos
#Calificacion las urls
    if Info_Twitters.enlaces_active:
	bcalificacion_enlaces = calificar_enlaces(lurls)
    else:
	bcalificacion_enlaces = None
	#Calificacion del idioma
    if Info_Twitters.idioma_active is not None:
	bcalificacion_idioma = calificar_idioma(Info_Twitters.idioma_active, lang)
    else:
	bcalificacion_idioma = None

	#Calificacion de las palabrotas
    if Info_Twitters.palabrotas_active:
	bcalificacion_palabrotas = calificacion_palabrotas(texto_tweet)
    else:
	bcalificacion_palabrotas = None

	#Calificacion la hora
    if Info_Twitters.restriccion_hora_min is not None:
	bcalificacion_hora = calificacion_hora(Info_Twitters.restriccion_hora_min, Info_Twitters.restriccion_hora_max, created_at)	
    else:
	bcalificacion_hora = None

	#Calificacion la ubicacion
    if Info_Twitters.ubicacion_active is not None:
	bcalificacion_ubicacion = calificacion_ubicacion(Info_Twitters.ubicacion_active, ubicacion)
    else:
	bcalificacion_ubicacion = None
    pasaFiltro = 2
	#No pasa el filtro
    if((bcalificacion_enlaces is not None)and(not(bcalificacion_enlaces))) or ((bcalificacion_idioma is not None)and(not(bcalificacion_idioma))) or ((bcalificacion_palabrotas is not None)and(not(bcalificacion_palabrotas)))or((bcalificacion_hora is not None)and(not(bcalificacion_hora)))or((bcalificacion_ubicacion is not None)and(not(bcalificacion_ubicacion))):
	if (Info_Twitters.borrar_active):
		pasaFiltro = 0
	else:
		pasaFiltro = 1
    engine.execute('INSERT INTO tweet_history (user_id, tweet_id, texto_tweet, autor_tweet, calificacion_enlaces, calificacion_idioma, calificacion_palabrotas, calificacion_hora, calificacion_ubicacion, created_at) VALUES (:user_id, :tweet_id, :texto_tweet, :autor, :bcalificacion_enlaces, :bcalificacion_idioma, :bcalificacion_palabrotas, :bcalificacion_hora, :bcalificacion_ubicacion, :created_at)', user_id=user_id, tweet_id=tweet_id, texto_tweet=texto_tweet, autor=autor, bcalificacion_enlaces=bcalificacion_enlaces, bcalificacion_idioma=bcalificacion_idioma, bcalificacion_palabrotas=bcalificacion_palabrotas, bcalificacion_hora=bcalificacion_hora, bcalificacion_ubicacion=bcalificacion_ubicacion, created_at=created_at)

    return pasaFiltro



    	


