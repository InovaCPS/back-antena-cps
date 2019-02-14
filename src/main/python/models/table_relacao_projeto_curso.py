from webapp import db

class Rel_projeto_curso(db.Model):
    __tablename__: 'rel_projeto_curso'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id'))

    def __init__(self, id_projeto, id_curso):
        self.id_projeto = id_projeto
        self.id_curso = id_curso