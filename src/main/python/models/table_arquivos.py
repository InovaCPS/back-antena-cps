from webapp import db

class Arquivo(db.Model):
    __tablename__: 'arquivos'

    id = db.Column(db.Integer, primary_key = True)
    midia = db.Column(db.String(500))
    titulo = db.Column(db.String(50))
    descricao = db.Column(db.String(250))
    codigo = db.Column(db.String(50))
    id_parceiro = db.Column(db.Integer, db.ForeignKey('parceiros.ig_geral'))

    def __init__(self, midia, titulo, descricao, codigo, id_parceiro):
        self.midia = midia
        self.titulo = titulo
        self.descricao = descricao
        self.codigo = codigo
        self.id_parceiro = id_parceiro