#   Date: 2018-07-10
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    This module provides a flask application responding
    to the endpoints of Logger.
"""

from functools import wraps

from flask import Flask, Response, request, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from helper.config_helper import ConfigHelper
from flasgger import Swagger

import sys
import os

'''

inovaBDUser = os.environ.get['INOVA_USER']
inovaBDPassword = os.environ.get['INOVA_PSWD']
inovaBDHost = os.environ.get['INOVA_HOST']
inovaBDPorta = os.environ.get['INOVA_PORT']
inovaBDDatasource = os.environ.get['INOVA_DB']


def config_db_url(resource):
    config = ConfigHelper(resource)
    url = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        db=inovaBDDatasource,
        host=inovaBDHost,
        port=inovaBDPorta,
        user=inovaBDUser,
        pw=inovaBDPassword
    )
    return url
'''

def config_db_url(resource):
    config = ConfigHelper(resource)
    url = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        db=config.get_property_by_section('datasource', 'inova.db.datasource'),
        host=config.get_property_by_section('datasource', 'inova.db.host'),
        port=config.get_property_by_section('datasource', 'inova.db.port'),
        user=config.get_property_by_section('datasource', 'inova.db.username'),
        pw=config.get_property_by_section('datasource', 'inova.db.password')
    )
    return url

def get_db_instance(application, db_url):
    application.config['SECRET_KEY'] = 'thisissecret'
    application.config['SQLALCHEMY_DATABASE_URI'] = db_url
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return SQLAlchemy(application)

# Se '-t' estiver na lista de parâmetros so sistema o arquivo de configuração do banco é alterado
# indicando que os testes estão sendo rodados, caso contrário as configurações do banco
# permanecem as mesmas
APP_RESOURCE = './src/main/resources/application.properties'
if '-t' in sys.argv:
    APP_RESOURCE = './src/main/resources/application_qa.properties'

DB_URL = config_db_url(APP_RESOURCE)
application = Flask(__name__)
api = Api(application)
CORS(application)
db = get_db_instance(application, DB_URL)

application.config['UPLOAD_FOLDER'] = '../arquivos/'

application.config['MAIL_SERVER']='*****'
application.config['MAIL_PORT'] = 587
application.config['MAIL_USERNAME'] = '*****'
application.config['MAIL_PASSWORD'] = '****'
application.config['MAIL_USE_TLS'] = True


mail = Mail(application)

cp = Blueprint('cp', __name__, url_prefix='/cp')

from models.table_parceiros import Parceiros

from views.central_parceiros.login import *
from views.central_parceiros.agentes import cp
from views.central_parceiros.eventos import cp
from views.central_parceiros.parceiros import cp
from views.central_parceiros.locais import cp
from views.central_parceiros.mensagem import cp
from views.central_parceiros.diretor import cp
from views.central_parceiros.diretor import cp
from views.central_parceiros.adm import cp
from views.central_parceiros.aluno import cp
from views.central_parceiros.projetos import cp

application.register_blueprint(cp)


#db.create_all()

application.config['SWAGGER'] = {
    'title': 'Antena CPS', 
    'description': '#InovaCPS, uma comunidade desenvolvendo a maior e melhor plataforma de conexão entre alunos e o ecossistema, faça parte desse hack!'
}
swagger = Swagger(application)