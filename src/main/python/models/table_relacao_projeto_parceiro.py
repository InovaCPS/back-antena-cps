from webapp import db

class Rel_projeto_colaborador(db.Model):
    __tablename__: 'rel_projeto_colaborador'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_colaborador = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))
    tipo = db.Column(db.String(50))

    def __init__(self, id_projeto, id_colaborador, tipo):
        self.id_projeto = id_projeto
        self.id_colaborador = id_colaborador
        self.tipo = tipo