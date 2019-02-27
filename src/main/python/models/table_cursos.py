from webapp import db

class Cursos(db.Model):
    __tablename__: 'cursos'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150))

    def __init__(self, nome):
        self.nome = nome