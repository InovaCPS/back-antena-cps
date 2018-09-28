from webapp import db

class Inscricoes(db.Model):
    __tablename__:'inscricoes'

    id = db.Column(db.Integer,primary_key=True)
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    id_eventos = db.Column(db.Integer, db.ForeignKey('eventos.id'))

    def __init__(self,id_parceiros,id_eventos):
        self.id_parceiros = id_parceiros
        self.id_eventos = id_eventos