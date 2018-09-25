from webapp import app
from models.table_parceiros import Parceiros
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decoreted(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']
        
        if not token:
            return jsonify({'messagem': 'Você precisa de uma Token para ter acesso!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Parceiros.query.filter_by(id_geral = data['id_geral']).first()
        except:
            return jsonify({'messagem': 'Token invalida!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decoreted


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    parceiro = Parceiros.query.filter_by(email = auth.username).first()

    if not parceiro:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(parceiro.senha, auth.password):
        token = jwt.encode({'id_geral': parceiro.id_geral, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 40)}, app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    

'''

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    global APP_RESOURCE
    config = ConfigHelper(APP_RESOURCE)
    auth_username = config.get_property_by_section('server', 'auth.username')
    auth_password = config.get_property_by_section('server', 'auth.password')
    return username == auth_username and password == auth_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
'''