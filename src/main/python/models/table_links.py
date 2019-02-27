from webapp import db

class Links(db.Model):
    __tablename__: 'links'

    id = db.Column(db.Integer, primary_key = True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('projetos.id'))
    url = db.Column(db.String(300))

    def __init__(self, id_projeto, url):
        self.id_projeto = id_projeto
        self.url = url