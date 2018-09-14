from webapp import db

class Atividade(db.Model):
    __tablename__:'atividade'

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    tipo = db.Column(db.String(100))
    duracao = db.Column(db.Integer)
    banner = db.Column(db.String(500))

    def __init__(self,titulo,descricao,tipo,duracao,banner):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.duracao = duracao
        self.banner = banner