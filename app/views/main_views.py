
from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash
from flask_user import current_user, login_required, roles_required
from app.extras.monitoring import levantartodoslosStreams, matartodoslosStreams
from app.models.user_models import UserConfigurationForm, Tweet_History, Info_Twitter
from app.extras.queries import *

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    if current_user.is_authenticated:
	return redirect(url_for('main.lista_tweets'))
    else: 
    	return redirect(url_for('user.login'))


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')

@main_blueprint.route('/levantar')
@roles_required('admin')
@login_required  # Limits access to authenticated users
def levantar():
    cont=levantartodoslosStreams()
    return render_template('main/streamsactivos.html',streamsactivos=cont)

@main_blueprint.route('/matar')
@roles_required('admin')
@login_required  # Limits access to authenticated users
def matartodos():
    cont=matartodoslosStreams()
    return render_template('main/streamsmuertos.html',streamsmuertos=cont)



# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/lista_tweets')
@login_required  # Limits access to authenticated users
def lista_tweets():
    ltweethistory=Tweet_History.query.filter(current_user.id==Tweet_History.user_id).order_by(Tweet_History.created_at.desc()).all()
    return render_template('main/lista_tweets.html',ltweets=ltweethistory)

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/configuracion')
@login_required  # Limits access to authenticated users
def configuracion():
    return render_template('main/configuracion.html')

@main_blueprint.route('/main/profile')
@login_required
def user_profile_page():
    infotwitter=Info_Twitter.query.filter(current_user.id==Info_Twitter.user_id).all()
    return render_template('main/cuentas.html', cuentas = infotwitter)

@main_blueprint.route('/main/profile/<idd>', methods=['GET','POST'])
@login_required
def cuentas_creadas_modificacion(idd):
    try:
	idd=int(idd)
	nueva_cuenta = idd==0
    except:
	return redirect(url_for('main.user_profile_page'))    
    infotwitter=Info_Twitter.query.filter(current_user.id==Info_Twitter.user_id).filter(idd==Info_Twitter.id).first()
    if (nueva_cuenta):
	infotwitter=Info_Twitter(user_id = 0,
			       usuario_twitter = u'',
                    	       iduser_twitter= u'',
                               consumer_key=u'', 
                               consumer_secret=u'', 
                               access_token=u'', 
                               access_token_secret= u'', 
			       enlaces_active=False,
			       idioma_active=None,
			       palabrotas_active=False,
			       restriccion_hora_min=None,
			       restriccion_hora_max=None,
			       ubicacion_active = None,
			       streamer_active = False,
			       borrar_active = False)
    elif(infotwitter is None):
	return redirect(url_for('main.user_profile_page'))  
    form = UserConfigurationForm(request.form, obj=current_user, nombre_twitter=infotwitter.usuario_twitter, consumer_key =infotwitter.consumer_key, consumer_secret = infotwitter.consumer_secret, access_token = infotwitter.access_token, access_token_secret= infotwitter.access_token_secret,idioma_active=infotwitter.idioma_active,ubicacion_active =infotwitter.ubicacion_active, streamer_active = infotwitter.streamer_active,  borrar_active = infotwitter.borrar_active) 

   # Process valid POST
    if request.method == 'POST' and form.validate():
	lerrores = find_or_create_InfoTwitter(idd, current_user.id, request)
	if lerrores != []:
		for error in lerrores:		
			flash(error)
		return render_template('main/user_profile_page.html',
                           form=form,enlaces_active = infotwitter.enlaces_active, palabrotas_active = infotwitter.palabrotas_active, restriccion_hora_min = infotwitter.restriccion_hora_min,  restriccion_hora_max = infotwitter.restriccion_hora_max, streamer_active = infotwitter.streamer_active, borrar_active = infotwitter.borrar_active)
	flash('Cambio de la Informacion de Twitter Realizado')
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form, enlaces_active = infotwitter.enlaces_active, palabrotas_active = infotwitter.palabrotas_active, restriccion_hora_min = infotwitter.restriccion_hora_min,  restriccion_hora_max = infotwitter.restriccion_hora_max, streamer_active = infotwitter.streamer_active, borrar_active = infotwitter.borrar_active) 


