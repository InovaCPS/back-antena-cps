from webapp import db

class Unidade(db.Model):
    __tablename__:'unidade'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(500))

    def __init__(self,nome,endereco):
        self.nome = nome
        self.endereco = endereco