from webapp import db

class Agentes(db.Model):
    __tablename__:'agentes'

    id = db.Column(db.Integer, primary_key = True)
    matricula = db.Column(db.String(10))
    id_unidades = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    id_regioes = db.Column(db.Integer, db.ForeignKey('regioes.id'))
    id_parceiros = db.Column(db.Integer, db.ForeignKey('parceiros.id_geral'))

    def __init__(self,matricula,id_unidades,id_regioes,id_parceiros):
        self.matricula = matricula
        self.id_unidades = id_unidades
        self.id_regioes = id_regioes
        self.id_parceiros = id_parceiros