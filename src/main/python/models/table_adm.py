from webapp import db

class Adm(db.Model):
    __tablename__ = 'adm'

    id = db.Column(db.Integer, primary_key = True)
    id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id_geral'))

    
    
    def __init__(self, id_usuarios):
        self.id_usuarios = id_usuarios
        