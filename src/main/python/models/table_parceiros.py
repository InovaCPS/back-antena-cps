from webapp import db
from flask_login import UserMixin

class Parceiros(UserMixin, db.Model):
    __tablename__:'parceiros'

    id_geral = db.Column(db.Integer,primary_key=True)

    nivel = db.Column(db.String(100))
    
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(50))

    email = db.Column(db.String(100), unique = True)
    senha = db.Column(db.String(500))

    cpf = db.Column(db.String(50))
    rg = db.Column(db.String(15))

    matricula = db.Column(db.Integer())

    foto_perfil = db.Column(db.String(500))

    dt_nascimento = db.Column(db.Date())
    genero = db.Column(db.String(15))
    
    local_trabalho = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    
    telefone = db.Column(db.String(20))
    lattes = db.Column(db.String(500))
    facebook = db.Column(db.String(500))
    linkedin = db.Column(db.String(500))
    twitter = db.Column(db.String(500))
    validado = db.Column(db.Boolean)

    def __init__(self, nivel, email, senha, validado):
        self.nivel = nivel
        self.email = email
        self.senha = senha
        self.validado = validado
       