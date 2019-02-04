from webapp import app, db
from models.table_parceiros import Parceiros
from flask import request, jsonify, make_response, redirect, url_for, session
from flask_cors import cross_origin
from werkzeug.security import check_password_hash
from werkzeug.wrappers import Response
from werkzeug.datastructures import Headers
import jwt
import datetime
from functools import wraps

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from models.table_oauth import OAuth
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_blueprint = make_google_blueprint(
    client_id="1092697945658-mm49tuj821b1a3jni5epplc0l54ofj0s.apps.googleusercontent.com",
    client_secret="XSK0EQfS9PEG3KN9bUySkjsz",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)

app.register_blueprint(google_blueprint, url_prefix='/google_login')
google_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user_required=False)

def token_required(f):
    @wraps(f)
    def decoreted(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        # if session['token']:
        #     token = session['token']
        
        if not token:
            return jsonify({'Mensagem': 'Você precisa de uma Token para ter acesso!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Parceiros.query.filter_by(id_geral = data['id_geral']).first()
        except:
            return jsonify({'Mensagem': 'Token invalida!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decoreted


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    parceiro = Parceiros.query.filter_by(email = auth['username']).first()

    if not parceiro:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(parceiro.senha, auth['password']):
        token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        
        # session['token'] = token.decode('UTF-8')
        # return jsonify({'Mensagem': 'Bem Vindo {}!'.format(parceiro.nome)})
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/login/google', methods=['GET', 'POST'])
@cross_origin()
def google_login():
    resp = redirect(url_for('google.login'))

    # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    # resp.headers = Headers({'Access-Control-Allow-Origin': 'http://localhost:4200'})
    # resp.headers = Headers.add_header('Access-Control-Allow-Origin', 'http://localhost:4200')
    resp.headers = {
        'Access-Control-Allow-Origin': '*', 
        'Location': 'http://localhost:8080/google_login/google'
    }
    # resp.headers.set('Access-Control-Allow-Origin', 'http://localhost:4200')
    # resp.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')

    return resp

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    account_info = blueprint.session.get('/oauth2/v2/userinfo')

    if account_info.ok:
        account_info_json = account_info.json()

        parceiro = Parceiros.query.filter_by(email=account_info_json['email']).first()

        if not parceiro:
            parceiro = Parceiros(
                nivel='Parceiro', 
                email=account_info_json['email'], 
                senha='Google account', 
                validado=False
            )
            db.session.add(parceiro)
            db.session.commit()

        
        token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        # response = make_response()
        # response.headers.set('Access-Control-Allow-Origin', '*')

        return jsonify({'token': token.decode('UTF-8')})