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

import sys

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


def get_db_instance(app, db_url):
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return SQLAlchemy(app)

# Se '-t' estiver na lista de parâmetros so sistema o arquivo de configuração do banco é alterado
# indicando que os testes estão sendo rodados, caso contrário as configurações do banco
# permanecem as mesmas
APP_RESOURCE = './src/main/resources/application.properties'
if '-t' in sys.argv:
    APP_RESOURCE = './src/main/resources/application_qa.properties'

DB_URL = config_db_url(APP_RESOURCE)
app = Flask(__name__)
api = Api(app)
CORS(app)
db = get_db_instance(app, DB_URL)

app.config['UPLOAD_FOLDER'] = '../arquivos/'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'senha gmail'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

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

app.register_blueprint(cp)