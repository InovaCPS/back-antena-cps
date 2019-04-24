from webapp import application, db
from models.table_parceiros import Parceiros
from flask import request, jsonify, make_response, redirect, url_for, session
from flask_cors import cross_origin
from werkzeug.security import check_password_hash
from werkzeug.wrappers import Response
from werkzeug.datastructures import Headers
import jwt
import datetime
from functools import wraps
from flasgger.utils import swag_from
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from models.table_oauth import OAuth
from sqlalchemy.orm.exc import NoResultFound

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


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
            data = jwt.decode(token, application.config['SECRET_KEY'])
            current_user = Parceiros.query.filter_by(id_geral = data['id_geral']).first()
        except:
            return jsonify({'Mensagem': 'Token invalida!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decoreted


@application.route('/login', methods=['POST'])
@swag_from('../swagger_specs/autenticacao/login.yml', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    parceiro = Parceiros.query.filter_by(email = auth['username']).first()

    if not parceiro:
        return jsonify({'Mensagem': 'Não foi possivel verificar'})
    
    if check_password_hash(parceiro.senha, auth['password']):
        token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, application.config['SECRET_KEY'])
        
        # session['token'] = token.decode('UTF-8')
        # return jsonify({'Mensagem': 'Bem Vindo {}!'.format(parceiro.nome)})
        return jsonify({'token': token.decode('UTF-8')})
    
    return jsonify({'Mensagem': 'Senha Incorreta!'})


@application.route('/login/google', methods=['POST'])
def google_login():
    account_info_json = request.get_json()

    parceiro = Parceiros.query.filter_by(email=account_info_json['email']).first()

    if not parceiro:
        parceiro = Parceiros(
            nivel='Parceiro', 
            email=account_info_json['email'], 
            senha='Google account', 
            validado=True
        )
        parceiro.nome = account_info_json['name']
        parceiro.sobrenome = account_info_json['lastName'] 

        db.session.add(parceiro)
        db.session.commit()


    token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, application.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')})
    


@application.route("/login/facebook", methods=['POST'])
def facebook_login():
    account_info_json = request.get_json()

    parceiro = Parceiros.query.filter_by(email = account_info_json['email'])

    if not parceiro:
        parceiro = Parceiros(
            nivel='Parceiro',
            email= account_info_json['email'], 
            senha='Facebook account', 
            validado= True
        )
        parceiro.nome = account_info_json['first_name']
        parceiro.sobrenome = account_info_json['last_name'] 
        db.session.add(parceiro)
        db.session.commit()

    token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, application.config['SECRET_KEY'])
    
    return jsonify({'token': token.decode('UTF-8')})     