from webapp import db

class Inscricoes(db.Model):
    __tablename__:'inscricoes'

    id = db.Column(db.Integer,primary_key=True)
    capacidade = db.Column(db.Integer)
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    id_eventos = db.Column(db.Integer, db.ForeignKey('eventos.id'))

    def __init__(self,capacidade,id_parceiros,id_eventos):
        self.capacidade = capacidade
        self.id_parceiros = id_parceiros
        self.id_eventos = id_eventos