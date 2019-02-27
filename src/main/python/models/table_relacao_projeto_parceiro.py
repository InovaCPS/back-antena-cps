from webapp import db

class Rel_projeto_colaborador(db.Model):
    __tablename__: 'rel_projeto_colaborador'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_colaborador = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))

    def __init__(self, id_projeto, id_colaborador):
        self.id_projeto = id_projeto
        self.id_colaborador = id_colaborador