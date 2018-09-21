from webapp import db
from models.table_unidades import Unidades
from models.table_atividades import Atividades

class Eventos(db.Model):
    __tablename__:'evento'

    id = db.Column(db.Integer, primary_key=True)
    id_atividades = db.Column(db.Integer,db.ForeignKey(Atividades.id))
    id_unidades = db.Column(db.Integer,db.ForeignKey(Unidades.id))
    _data = db.Column(db.Date())
    hora = db.Column(db.Time())

    def __init__(self,id_atividades,id_unidades,_data,hora):
        self.id_atividades = id_atividades
        self.id_unidades = id_unidades
        self._data = _data
        self.hora = hora