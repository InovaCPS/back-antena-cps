from webapp import app
from models.table_parceiros import Parceiros
from flask import request, jsonify, make_response, session, redirect, url_for
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decoreted(*args, **kwargs):
        token = None

        #if 'token' in request.headers:
            #token = request.headers['token']

        if session['token']:
            token = session['token']
        
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
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    parceiro = Parceiros.query.filter_by(email = auth.username).first()

    if not parceiro:
        return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(parceiro.senha, auth.password):
        token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        
        session['token'] = token.decode('UTF-8')
        return jsonify({'Mensagem': 'Bem Vindo {}!'.format(parceiro.nome)})
        #return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Não foi possivel verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})