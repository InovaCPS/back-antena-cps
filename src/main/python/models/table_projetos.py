from webapp import db

class Projeto(db.Model):
    __tablename__: 'projetos'

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    id_parceiro = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    premiado = db.Column(db.Boolean)

    def __init__(self, titulo, descricao, id_parceiro, premiado):
        self.titulo = titulo
        self.descricao = descricao
        self.id_parceiro = id_parceiro
        self.premiado = premiado