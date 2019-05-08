from webapp import db

class Arquivos(db.Model):
    __tablename__: 'arquivos'

    id = db.Column(db.Integer, primary_key = True)
    tipo = db.Column(db.String(30))
    titulo = db.Column(db.String(50))
    descricao = db.Column(db.String(250))
    codigo = db.Column(db.String(50))
    id_parceiro = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))

    def __init__(self, tipo, titulo, descricao, codigo, id_parceiro):
        self.tipo = tipo
        self.titulo = titulo
        self.descricao = descricao
        self.codigo = codigo
        self.id_parceiro = id_parceiro