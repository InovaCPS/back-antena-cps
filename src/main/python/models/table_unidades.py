from webapp import db

class Unidades(db.Model):
    __tablename__:'unidades'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(500))
    id_regioes = db.Column(db.Integer, db.ForeignKey('regioes.id'))

    def __init__(self,nome,endereco,id_regioes):
        self.nome = nome
        self.endereco = endereco
        self.id_regioes = id_regioes