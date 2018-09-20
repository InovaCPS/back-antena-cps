from webapp import db

class Parceiro_tema(db.Model):
    __tablename__: 'parceiro_tema'

    id = db.Column(db.Integer, primary_key = True)
    id_tema = db.Column(db.Integer, db.ForeignKey('tema_interesse.id'))
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiro.id'))

    def __init__(self,id_tema,id_parceiros):
        self.id_tema = id_tema
        self.id_parceiros = id_parceiros