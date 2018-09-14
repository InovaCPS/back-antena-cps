from webapp import db
from models.table_unidade import Unidade
from models.table_atividade import Atividade

class Evento(db.Model):
    __tablename__:'evento'

    id = db.Column(db.Integer, primary_key=True)
    atividade = db.Column(db.Integer,db.ForeignKey(Atividade.id))
    unidade = db.Column(db.Integer,db.ForeignKey(Unidade.id))
    _data = db.Column(db.Date())
    hora = db.Column(db.Time())

    def __init__(self,atividade,unidade,_data,hora):
        self.atividade = atividade
        self.unidade = unidade
        self._data = _data
        self.hora = hora