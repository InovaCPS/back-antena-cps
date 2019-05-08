from webapp import db

class Rel_Curso_Unidade(db.Model):
    __tablename__: 'rel_curso_unidade'

    id = db.Column(db.Integer, primary_key = True)
    id_curso = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidades.id'))


    def __init__(self, id_projeto, id_curso):
        self.id_projeto = id_projeto
        self.id_curso = id_curso