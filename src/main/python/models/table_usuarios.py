from webapp import db

class Usuarios(db.Model):
    __tablename__:'usuarios'

    id_geral = db.Column(db.Integer,primary_key=True)

    nivel = db.Column(db.String(100))
    
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(500))

    cpf = db.Column(db.String(50))
    rg = db.Column(db.String(15))

    dt_nascimento db.Column(db.Date())
    genero = db.Column(db.String(15))
    
    hora = db.Column(db.Time())
    local_trabalho = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    local_estudo = db.Column(db.String(100))
    
    telefone = db.Column(db.String(20))
    lattes = db.Column(db.String(500))
    facebook = db.Column(db.String(500))
    linkedin = db.Column(db.String(500))
    twitter = db.Column(db.String(500))

    def __init__(self,nivel,nome,email,senha,cpf,rp,dt_nascimento,genero,hora,local_trabalho,cargo,local_estudo,telefone,lattes,facebook,linkedin,twitter):
        self.nivel = nivel
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.rp = rp
        self.dt_nascimento = dt_nascimento
        self.genero = genero
        self.hora = hora
        self.local_trabalho = local_trabalho
        self.cargo = cargo
        self.local_estudo = local_estudo
        self.telefone = telefone
        self.lattes = lattes
        self.facebook = facebook
        self.linkedin = linkedin
        self.twitter = twitter