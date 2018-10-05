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
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from helper.config_helper import ConfigHelper


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




APP_RESOURCE = './src/main/resources/application.properties'
DB_URL = config_db_url(APP_RESOURCE)
app = Flask(__name__)
api = Api(app)
CORS(app)
db = get_db_instance(app, DB_URL)

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

app.register_blueprint(cp)

from models.table_evento import Eventos

def check_eventos():
    from datetime import time, datetime
    eventos = Eventos.query.filter_by(_data=datetime.today())

    for evento in eventos:
        agora = datetime.now()
        agendamento = datetime(
            year = evento._data.year, 
            month = evento._data.month, 
            day = evento._data.day, 
            hour = evento.hora.hour, 
            minute = evento.hora.minute
        )

        agora = datetime.now()

        if agora < agendamento and agendamento.hour - agora.hour == 1:
            evento.acesso = False
            db.session.commit()


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=check_eventos,
    trigger=IntervalTrigger(minutes=1),
    replace_existing=True
)
atexit.register(lambda: scheduler.shutdown())
