from webapp import db

class Projetos(db.Model):
    __tablename__: 'projetos'

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    descricao = db.Column(db.String(500))
    orientador = db.Column(db.String(100))
    status = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    tema = db.Column(db.String(100))
    textoProjeto = db.Column(db.String(1000))
    linkTexto = db.Column(db.String(200))
    capa = db.Column(db.LargeBinary)

    def __init__(self, titulo, descricao, orientador, status, tipo, tema):
        self.titulo = titulo
        self.descricao = descricao
        self.orientador = orientador
        self.status = status
        self.tipo = tipo
        self.tema = tema