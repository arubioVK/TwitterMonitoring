
import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role, Info_Twitter, Tweet_History

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user1 = find_or_create_user(u'admin@admin.com', '1', admin_role)
    
    # Save to DB
    db.session.commit()

def find_or_create_Info_Twitter (user, usuario_twitter,iduser_twitter, consumer_key, consumer_secret, access_token, access_token_secret, enlaces_active=0, idioma_active = None, palabrotas_active =0, restriccion_hora_min = None, restriccion_hora_max= None, ubicacion_active=0, streamer_active=0 , borrar_active =0):
    Info_Twitters = Info_Twitter.query.filter(Info_Twitter.user_id ==user.id).first()
    if not Info_Twitters:
	Info_Twitters = Info_Twitter(user_id = user.id,
			       usuario_twitter = usuario_twitter,
                    	       iduser_twitter= iduser_twitter,
                               consumer_key=consumer_key, 
                               consumer_secret=consumer_secret, 
                               access_token=access_token, 
                               access_token_secret= access_token_secret, 
			       enlaces_active=enlaces_active,
			       idioma_active=idioma_active,
			       palabrotas_active=palabrotas_active,
			       restriccion_hora_min=restriccion_hora_min,
			       restriccion_hora_max=restriccion_hora_max,
			       ubicacion_active = ubicacion_active,
			       streamer_active = streamer_active)
	db.session.add(Info_Twitters)
    return Info_Twitters

def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def create_tweet(user,tweet_id, texto_tweet, autor_tweet, calificacion_enlaces, calificacion_idioma, calificacion_palabrotas, calificacion_hora, calificacion_ubicacion, created_at):
    tweet_history = Tweet_History(user_id = user.id,tweet_id = tweet_id, texto_tweet = texto_tweet, autor_tweet = autor_tweet, calificacion_enlaces= calificacion_enlaces, calificacion_idioma = calificacion_idioma, calificacion_palabrotas=calificacion_palabrotas, calificacion_hora=calificacion_hora, calificacion_ubicacion = calificacion_ubicacion, created_at = created_at )
    db.session.add(tweet_history)


def extraemeuser(iduserbbdd):	
    return User.query.filter(User.id == iduserbbdd).first()



