from webapp import db

class Rel_projeto_categoria(db.Model):
    __tablename__: 'rel_projeto_categoria'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_projetos.id'))

    def __init__(self, id_projeto, id_categoria):
        self.id_projeto = id_projeto
        self.id_categoria = id_categoria