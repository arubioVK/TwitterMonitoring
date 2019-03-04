
from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, SubmitField, validators
from wtforms.validators import ValidationError
from app import db
import re


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    # Relationships
    
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes



# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Info_Twitter(db.Model):
    __tablename__ = 'info_twitter'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    usuario_twitter = db.Column(db.String(255), nullable=False, server_default='')
    iduser_twitter = db.Column(db.String(255), nullable=False, server_default=u'')
    consumer_key = db.Column(db.String(255), nullable=False, server_default='')
    consumer_secret = db.Column(db.String(255), nullable=False, server_default='')
    access_token = db.Column(db.String(255), nullable=False, server_default='')
    access_token_secret = db.Column(db.String(255), nullable=False, server_default='')
    enlaces_active = db.Column(db.Boolean(), nullable=False, server_default='0')
    idioma_active = db.Column(db.String(50))
    palabrotas_active = db.Column(db.Boolean(), nullable=False, server_default='0')
    restriccion_hora_min = db.Column(db.DateTime())
    restriccion_hora_max = db.Column(db.DateTime())
    ubicacion_active = db.Column(db.String(50))
    streamer_active = db.Column(db.Boolean(), nullable=False, server_default='0')
    borrar_active = db.Column(db.Boolean(), nullable=False, server_default='0')

class Tweet_History(db.Model):
    __tablename__ = 'tweet_history'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.String(255), nullable=False, server_default='')
    texto_tweet = db.Column(db.String(255), nullable=False, server_default='')
    autor_tweet = db.Column(db.String(255), nullable=False, server_default='')
    calificacion_enlaces = db.Column(db.Boolean())
    calificacion_idioma = db.Column(db.Boolean())
    calificacion_palabrotas = db.Column(db.Boolean())
    calificacion_hora = db.Column(db.Boolean())
    calificacion_ubicacion = db.Column(db.Boolean()) 
    created_at = db.Column(db.DateTime())


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')

class UserConfigurationForm(FlaskForm):
    nombre_twitter = StringField('Usuario de Twitter', validators=[
        validators.DataRequired('Usuario de Twitter es Necesario')])
    consumer_key = StringField('Consumer Key', validators=[
        validators.DataRequired('Consumer Key is required')])
    consumer_secret = StringField('Consumer Secret', validators=[
        validators.DataRequired('Consumer Secret is required')])
    access_token = StringField('Access Token', validators=[
        validators.DataRequired('Access Token is required')])
    access_token_secret = StringField('Access Token Secret', validators=[
        validators.DataRequired('Access Token Secret is required')])   
    enlaces_active = BooleanField('Enlaces maliciosos')
    idioma_active = SelectField('Lenguaje', choices = [('',''),('es', 'Espanol'),('en', 'English'),('fr', 'Francais'),('de', 'Deutsch'),('it','Italiano')]) 
    palabrotas_active = BooleanField('Antilenguaje ofensivo')
    restriccion_hora_min = StringField('Inicio Horario Permitido (GMT+0)')
    restriccion_hora_max = StringField('Fin Horario Permitido (GMT+0)')
    ubicacion_active = SelectField('Ubicacion', choices = [('',''),('US', 'United States'),('ES', 'Espana'),('PT','Portugal'),('FR','France'),('GB','United Kingdom'),('DE','Germany'),('IT','Italy')])
    streamer_active = BooleanField('Activar Servicio de Monitorizacion')
    borrar_active = BooleanField('Borrar Tweets en caso de no cumplir patron')
    submit = SubmitField('Save')




