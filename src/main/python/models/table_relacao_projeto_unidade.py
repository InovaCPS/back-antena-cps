from webapp import db

class Rel_projeto_unidade(db.Model):
    __tablename__: 'rel_projeto_unidade'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidades.id'))

    def __init__(self, id_projeto, id_unidade):
        self.id_projeto = id_projeto
        self.id_unidade = id_unidade