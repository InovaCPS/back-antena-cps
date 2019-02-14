from webapp import db

class Rel_projeto_arquivo(db.Model):
    __tablename__: 'rel_projeto_arquivo'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_arquivo = db.Column(db.Integer, db.ForeignKey('arquivos.id'))

    def __init__(self, id_projeto, id_arquivo):
        self.id_projeto = id_projeto
        self.id_arquivo = id_arquivo