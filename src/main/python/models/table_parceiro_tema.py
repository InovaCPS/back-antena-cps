from webapp import db

class Parceiro_tema(db.Model):
    __tablename__: 'parceiro_tema'

    id = db.Column(db.Integer, primary_key = True)
    id_tema = db.Column(db.Integer, db.ForeignKey('tema_interesse.id'))
    id_alunos = db.Column(db.Integer, db.ForeignKey('alunos.id'))

    def __init__(self,id_tema,id_alunos):
        self.id_tema = id_tema
        self.id_alunos = id_alunos