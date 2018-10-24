from webapp import db

class Unidades(db.Model):
    __tablename__:'unidades'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(300))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    id_regioes = db.Column(db.Integer, db.ForeignKey('regioes.id'))

    def __init__(self,nome,endereco,bairro,cidadeid_regioes):
        self.nome = nome
        self.endereco = endereco
        self.bairro = bairro
        self.cidade = cidade
        self.id_regioes = id_regioes