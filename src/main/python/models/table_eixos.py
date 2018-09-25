from webapp import db

class Eixos(db.Model):
    __tablename__:'eixos'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))

    def __init__(self,nome):
        self.nome = nome