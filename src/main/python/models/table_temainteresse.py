from webapp import db

class TemaInteresse(db.Model):
    __tablename__: 'temainteresse'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), unique = True)
    #parceiros = db.relationship('Parceiro_tema', backref='tema')

    def __init__(self, nome):
        self.nome = nome