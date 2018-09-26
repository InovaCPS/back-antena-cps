from webapp import db
from models.table_agentes import Agentes
from models.table_eixos import Eixos

class Atividades(db.Model):
    __tablename__:'atividades'

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    tipo = db.Column(db.String(100))
    duracao = db.Column(db.Integer)
    banner = db.Column(db.String(500))
    id_agente = db.Column(db.Integer, db.ForeignKey(Agentes.id))
    id_eixo = db.Column(db.Integer, db.ForeignKey(Eixos.id))
    id_parceiro = db.Column(db.Integer, db.ForeignKey(Parceiros.id))


    def __init__(self,titulo,descricao,tipo,duracao,banner,id_agente,id_parceiro):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.duracao = duracao
        self.banner = banner
        self.id_agente = id_agente
        self.id_parceiro = id_parceiro
        