from webapp import db
from models.table_atividades import Atividades
class Materiais(db.Model):
    __tablename__ = 'materiais'

    id = db.Column(db.Integer, primary_key = True)
    id_atividades = db.Column(db.Integer, db.ForeignKey(Atividades.id))
    materia = db.Column(db.String(500))

    def __init__(self, id_atividades, materia):
        self.id_atividades = id_atividades
        self.materia = materia