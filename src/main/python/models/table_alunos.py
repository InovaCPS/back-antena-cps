
from webapp import db

class Alunos(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key = True)
    ra = db.Column(db.Integer, unique = True)
    id_unidades = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))

    
    
    def __init__(self, ra, id_unidades, id_parceiros):
        self.ra = ra
        self.id_unidades = id_unidades
        self.id_parceiros = id_parceiros
        