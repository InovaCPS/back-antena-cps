
from webapp import db
from models.table_parceiro_tema import Parceiro_tema
class Parceiro(db.Model):
    __tablename__ = 'parceiro'

    id = db.Column(db.Integer, primary_key = True)
    aluno = db.Column(db.Boolean)
    ra = db.Column(db.Integer, unique = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    cpf = db.Column(db.String(50), unique = True)
    senha = db.Column(db.String(200))    

    rg = db.Column(db.String(15), unique = True)
    dt_nascimento = db.Column(db.Date())
    genero = db.Column(db.String(15))
    telefone = db.Column(db.String(20))
    local_trabalho = db.Column(db.String(100))
    local_estudo = db.Column(db.String(100))
    
    lattes = db.Column(db.String(500))
    facebook = db.Column(db.String(500))
    linkedin = db.Column(db.String(500))
    twitter = db.Column(db.String(500))

    #temas = db.relationship(Parceiro_tema, backref='parceiro')
    
    def __init__(self, aluno, ra, nome, email, cpf, senha):
        self.aluno = aluno
        self.ra = ra
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha

        '''self.rg = rg
        self.dt_nascimento = dt_nascimento
        self.genero = genero
        self.telefone = telefone
        self. local_trabalho = local_trabalho
        self.local_estudo = local_estudo
        self.lattes = lattes
        self.facebook = facebook
        self.linkedin - linkedin
        self.twitter = twitter'''
        