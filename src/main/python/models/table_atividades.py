from webapp import db
from models.table_agentes import Agentes

class Atividades(db.Model):
    __tablename__:'atividades'

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    tipo = db.Column(db.String(100))
    duracao = db.Column(db.Integer)
    banner = db.Column(db.String(500))
    id_agente = db.Column(db.Integer, db.ForeignKey(Agentes.id))
    id_eixo = db.Column(db.Integer, db.ForeignKey('eixos.id'))


    def __init__(self,titulo,descricao,tipo,duracao,banner, id_agente, id_eixo):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.duracao = duracao
        self.banner = banner
        self.id_agente = id_agente
        self.id_eixo = id_eixo
        