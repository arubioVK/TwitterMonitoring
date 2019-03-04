#! usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
from tweepy import OAuthHandler

#Extraemos ID User Twitter
#Además aprovechamos si las claves introducidas son correctas
def obtenerIDtwitter(nombreuser, ckey, csecret, atoken, asecret):
	try:
		auth = OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)
		api = tweepy.API(auth)
		usuario = api.get_user(screen_name = nombreuser)
		return (True,usuario.id)
	except:
		return (False,0)



