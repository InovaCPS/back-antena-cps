from webapp import db

class Avaliacoes(db.Model):
    __tablename__:'avaliacoes'

    id = db.Column(db.Integer,primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    id_parceiro = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    nota = db.Column(db.Float)
    comentario = db.Column(db.String)
    identificar = db.Column(db.Boolean)

    def __init__(self, id_evento, id_parceiro, nota, comentario, identificar):
        self.id_evento = id_evento
        self.id_parceiro = id_parceiro
        self.nota = nota
        self.comentario = comentario
        self.identificar = identificar