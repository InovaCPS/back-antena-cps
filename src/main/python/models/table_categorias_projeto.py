from webapp import db

class Categorias_projetos(db.Model):
    __tablename__:'categorias_projetos'

    id = db.Column(db.Integer, primary_key = True)
    categoria = db.Column(db.String(100))

    def __init__(self, categoria):
        self.categoria = categoria