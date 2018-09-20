
from webapp import db

class Parceiros(db.Model):
    __tablename__ = 'parceiros'

    id = db.Column(db.Integer, primary_key = True)
    aluno = db.Column(db.Boolean)
    ra = db.Column(db.Integer, unique = True)
    id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id_geral'))

    
    
    def __init__(self, aluno, ra, id_usuarios):
        self.aluno = aluno
        self.ra = ra
        self.id_usuarios = id_usuarios
        