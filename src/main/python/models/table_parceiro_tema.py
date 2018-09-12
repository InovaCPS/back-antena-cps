from webapp import db

class Parceiro_tema(db.Model):
    __tablename__: 'parceiro_tema'

    id = db.Column(db.Integer, primary_key = True)
    parceiro = db.Column(db.Integer, db.ForeignKey('parceiro.id'))
    tema = db.Column(db.Integer, db.ForeignKey('tema_interesse.id'))

    def __init__(self, parceiro, tema):
        self.parceiro = parceiro
        self.tema = tema