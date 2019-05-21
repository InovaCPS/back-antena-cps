from webapp import db

class Rel_projeto_detalhe(db.Model):
    __tablename__: 'rel_projeto_detalhe'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))

    categoria1 = db.Column(db.String(50))
    categoria2 = db.Column(db.String(50))

    premio1 = db.Column(db.String(50))
    premio2 = db.Column(db.String(50))

    recurso1 = db.Column(db.String(50))
    recurso2 = db.Column(db.String(50))

    credito1 = db.Column(db.String(50))
    credito2 = db.Column(db.String(50))

    direitos = db.Column(db.String(50))
    


    def __init__(self, id_projeto, categoria1, categoria2, recurso1, recurso2, premio1, premio2, credito1, credito2, direitos):
        self.id_projeto = id_projeto
        self.categoria1 = categoria1
        self.categoria2 = categoria2
        self.recurso1 = recurso1
        self.recurso2 = recurso2
        self.premio1 = premio1
        self.premio2 = premio2
        self.credito1 = credito1
        self.credito2 = credito2
        self.direitos = direitos