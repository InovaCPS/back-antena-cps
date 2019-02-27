from webapp import db

class Palavras_chave(db.Model):
    __tablename__: 'palavras_chave'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    palavra = db.Column(db.String(30))

    def __init__(self, id_projeto, palavra):
        self.id_projeto = id_projeto
        self.palavra = palavra