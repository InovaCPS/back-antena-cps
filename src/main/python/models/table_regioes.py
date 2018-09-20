from webapp import db

class Regioes(db.Model):
    __tablename__:'regioes'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))

    def __init__(self,nome):
        self.nome = nome