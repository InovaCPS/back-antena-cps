from webapp import db

class Materiais(db.Model):
    __tablename__ = 'materiais'

    id = db.Column(db.Integer, primary_key = True)
    id_atividades = db.Column(db.Integer, db.ForeignKey('atividades.id'))
    materia = db.Column(db.String(500))

    def __init__(self, id_atividades, materia):
        self.id_atividades = id_atividades
        self.materia = materia