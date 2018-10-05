from webapp import db
from models.table_unidades import Unidades
from models.table_atividades import Atividades
from models.table_diretores import Diretores

class Eventos(db.Model):
    __tablename__:'eventos'

    id = db.Column(db.Integer, primary_key=True)
    id_atividades = db.Column(db.Integer,db.ForeignKey(Atividades.id))
    id_unidades = db.Column(db.Integer,db.ForeignKey(Unidades.id))
    _data = db.Column(db.Date())
    hora = db.Column(db.Time())
    situacao = db.Column(db.String(40))
    capacidade = db.Column(db.Integer)
    inscrito = db.Column(db.Integer)
    acesso = db.Column(db.Boolean)


    def __init__(self,id_atividades,id_unidades,_data,hora, situacao, acesso):
        self.id_atividades = id_atividades
        self.id_unidades = id_unidades
        self._data = _data
        self.hora = hora
        self.situacao = situacao
        self.acesso = acesso