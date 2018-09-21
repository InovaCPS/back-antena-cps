from webapp import db

class Diretores(db.Model):
    __tablename__ = 'diretores'

    id = db.Column(db.Integer, primary_key = True)
    id_unidades = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))

    
    
    def __init__(self, id_unidades, id_parceiros):
        self.id_unidades = id_unidades
        self.id_parceiros = id_parceiros
        