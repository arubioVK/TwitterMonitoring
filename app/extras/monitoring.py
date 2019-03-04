#! usr/bin/python
# -*- coding: utf-8 -*-

import tweepy, threading, time, json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from app.extras.emails import enviarEmailBorradoTweet
from app.models.user_models import User
from app.extras.analisis import calificar_almacenar_tweet, calificar_almacenar_rt
from app.models.user_models import Info_Twitter
from app.__init__ import dameBBDD
from sqlalchemy import create_engine
import smtplib

dStreams ={}

def levantartodoslosStreams():
	lInfo_twitter = Info_Twitter.query.filter(Info_Twitter.streamer_active).all()
	cont = 0
	for infotwitter in lInfo_twitter:
		auth=loginTweet(infotwitter.consumer_key, infotwitter.consumer_secret, infotwitter.access_token, infotwitter.access_token_secret)
		t1 = backgroundstream(auth, infotwitter.iduser_twitter, infotwitter.id, infotwitter.user_id)
		t1.start()
		cont+=1
	print('Hay '+str(cont)+' Streams funcionando')
	return cont

def matartodoslosStreams():
	cont=0
	for idbbdd in dStreams.keys():
		matarStream(idbbdd)
		cont+=1
	return cont	

class backgroundstream(threading.Thread):
	def __init__(self, auth, iduser_twitter, idbbdd, id_userbbdd):
		threading.Thread.__init__(self)
		self.auth = auth
		self.iduser_twitter = iduser_twitter
		self.idbbdd = idbbdd
		self.id_userbbdd = id_userbbdd

	def run(self):
		print('Levantamos monitoreo ')
		monitoreartwitter(self.auth, self.iduser_twitter, self.idbbdd, self.id_userbbdd)

class listener(StreamListener):
   
    def __init__(self, aut, idbbdd, id_userbbdd):
	self.aut = aut
	self.idbbdd = idbbdd
	self.id_userbbdd = id_userbbdd
	self.engine = create_engine('sqlite:///app.sqlite')

    def on_data(self, data):
	try:
	    tweet = json.loads(data)
	    if tweet.get('delete') is not None:
		print('Es un mensaje de borrado')
	    elif tweet.get('retweeted_status') is not None:
		print('Ha llegado el siguiente RT: '+tweet.get('text'))
		resultado_calificacion = calificar_almacenar_rt(self.idbbdd, self.id_userbbdd, tweet, self.engine)
		if (resultado_calificacion == 0):
		    print('Borramos ese RT')
                    borrartweet(self.aut,tweet.get('id_str'))
		    result=self.engine.execute('SELECT * FROM users where id=:idd', idd=self.id_userbbdd).first()
		    subject ="RT Deshecho"
		    body="Hola,\nHemos deshecho tu ultimo RT, porque no cumple las condiciones configuradas en el Twitter Monitoring."
	            enviarEmailBorradoTweet(result.email, subject, body)
		elif (resultado_calificacion == 1):
		    print('Avisamos del RT')
		    result=self.engine.execute('SELECT * FROM users where id=:idd', idd=self.id_userbbdd).first()
		    subject ="RT Sospechoso"
		    body ="Hola,\nHemos detectado en tu ultimo RT, no cumple las condiciones configuradas en el Twitter Monitoring."
	            enviarEmailBorradoTweet(result.email, subject, body)
		print('Fin Analisis RT')
	    else:
		print('Ha llegado el siguiente mensaje: '+tweet.get('text'))
		resultado_calificacion = calificar_almacenar_tweet(self.idbbdd, self.id_userbbdd, tweet, self.engine)
		if (resultado_calificacion == 0):
		    print('Borramos ese mensaje')
                    borrartweet(self.aut,tweet.get('id_str'))
		    result=self.engine.execute('SELECT * FROM users where id=:idd', idd=self.id_userbbdd).first()
		    subject ="Tweet Borrado"
		    body ="Hola,\nHemos borrado el ultimo tweet que has generado, porque no cumple las condiciones configuradas en el Twitter Monitoring."
	            enviarEmailBorradoTweet(result.email, subject, body)
		elif (resultado_calificacion ==1):
		    print('Avisamos del Tweet')
		    result=self.engine.execute('SELECT * FROM users where id=:idd', idd=self.id_userbbdd).first()
		    subject ="Tweet Sospechoso"
		    body= "Hola,\nHemos detectado que en el ultimo tweet que has generado, no cumple las condiciones configuradas en el Twitter Monitoring."
	            enviarEmailBorradoTweet(result.email, subject, body)			
		print('Fin Analisis Tweet')
	except Exception as e:
	    print('Error recibido ->')
	    print(tweet)
	    print('<-Error finalizado')
	finally:
	    return(True)

    def on_error(self, status):
        print status

def loginTweet(ckey, csecret, atoken, asecret):
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	return auth

def obtenerIDtwitter(auth, nombreuser):
	try:
	    api = tweepy.API(auth)
	#Obtener el ID del usuario
	    user = api.get_user(screen_name = nombreuser)
	    return (True, user.id_str)
	except:
	    return (False,0)

def monitoreartwitter(auth, userid, idbbdd, id_userbbdd):
	#Monitorear twitter
	twitterStream = Stream(auth, listener(auth, idbbdd, id_userbbdd))
	dStreams.update({idbbdd:twitterStream})
	twitterStream.filter(follow=[userid])

def borrartweet(auth,id_tweet):
	api = tweepy.API(auth)
	api.destroy_status(id_tweet)

def matarStream(idd):
	stream = dStreams.pop(idd)
	stream.disconnect()

		







