from webapp import db
from models.table_atividade import Atividade
class Material(db.Model):
    __tablename__ = 'material'

    id = db.Column(db.Integer, primary_key = True)
    atividade = db.Column(db.Integer, db.ForeignKey(Atividade.id))
    materia = db.Column(db.String(500))

    def __init__(self, atividade, materia):
        self.atividade = atividade
        self.materia = materia