from webapp import db

class Mensagens(db.Model):
    __tablename__:'mensagens'

    id = db.Column(db.Integer,primary_key=True)
    descricao = db.Column(db.String(500))
    visualizacao = db.Column(db.String(50))
    id_remetentes = db.Column(db.Integer, db.ForeignKey('usuarios.id_geral'))
    id_destinatarios = db.Column(db.Integer, db.ForeignKey('usuarios.id_geral'))

    def __init__(self,descricao,visualizacao,id_remetentes,id_destinatarios):
        self.descricao = descricao
        self.visualizacao = visualizacao
        self.id_remetentes = id_remetentes
        self.id_destinatarios = id_destinatarios