from webapp import db

class Avaliacoes(db.Model):
    __tablename__:'avaliacoes'

    id = db.Column(db.Integer,primary_key=True)
    tipo_avaliado = db.Column(db.String) #**
    id_evento = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    id_avaliado = db.Column(db.Integer)
    id_avaliador = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    nota = db.Column(db.Float)
    comentario = db.Column(db.String)
    identificar = db.Column(db.Boolean)

    def __init__(self,tipo_avaliado, id_evento, id_avaliado, id_avaliador, nota, comentario, identificar):
        self.tipo_avaliado = tipo_avaliado
        self.id_evento = id_evento
        self.id_avaliado = id_avaliado
        self.id_avaliador = id_avaliador
        self.nota = nota
        self.comentario = comentario
        self.identificar = identificar


#** 
# se diretor avalia palestrante = Palestrante
# se Parceiro avalia evento =  Evento  
# se palestrante avalia unidade = Unidade