from webapp import app, db
from models.parceiro import Parceiro
from models.table_atividade import Atividade
from models.table_evento import Evento
from models.table_material import Material
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

cp = Blueprint('cp', __name__, url_prefix = '/cp')

#======================== ROTAS DE PARCEIROS =============================
@cp.route('/parceiro', methods=['GET'])
def get_parceiro():
    #pesquisar todos os parceiros no BD e gerar e exibir um json geral, com todos os parceiros
    dados = Parceiro.query.all()
    
    parceiros = []

    for info in dados:
        parceiro = {}
        parceiro['id'] = info.id
        parceiro['ra'] = info.ra
        parceiro['aluno'] = info.aluno
        parceiro['nome'] = info.nome
        parceiro['email'] = info.email
        parceiro['cpf'] = info.cpf
        
        parceiros.append(parceiro)

    return jsonify(parceiros)

@cp.route('/parceiro/<parceiro_id>', methods=['GET'])
def get_one_parceiro(parceiro_id):
    #pesquisar no BD um parceiro expecifico e gerar e exibir um json com todos os dados desse parceiro!
    info = Parceiro.query.filter_by(id = parceiro_id).first()

    if not info:
        return jsonify({'message': 'Não encontrado!'})

    parceiro = {}
    parceiro['id'] = info.id
    parceiro['ra'] = info.ra
    parceiro['aluno'] = info.aluno
    parceiro['nome'] = info.nome
    parceiro['email'] = info.email
    parceiro['cpf'] = info.cpf

    return jsonify(parceiro)

@cp.route('/parceiro', methods=['POST'])
def post_parceiro():
    #Cadastro de parceiro via json, com retorno de mensagem tambem via json
    #generate_password_hash serve para criptografar a senha
    #As condições são utilizadas para verificar se o parceiro informou o RA, caso o tenha feito
    #ele é cadastrado como aluno
    #Ex:
    #{"ra": "123456789", "nome": "aluno", "email": "email@email.com", "cpf": "11111111", "senha": "1234"}
    #{"ra": "", "nome": "ñ aluno", "email": "gmail@gmail.com", "cpf": "123456789", "senha": "1234"}
    
    data = request.get_json()   
    password = generate_password_hash(data['senha'])

    if not data['ra']:
       parceiro = Parceiro(aluno = False, ra = None, nome = data['nome'], email = data['email'], cpf = data['cpf'], senha = password)
    else:
        parceiro = Parceiro(aluno = True, ra = data['ra'], nome = data['nome'], email = data['email'], cpf = data['cpf'], senha = password)
    
    db.session.add(parceiro)
    db.session.commit()

    return jsonify({'message': 'Adicionado com sucesso!'})



@cp.route('/parceiro/<parceiro_id>', methods=['PUT'])
def edit_parceiro(parceiro_id):
    #alterar o usuario para aluno, caso ele tenha inserido o RA
    #Ex: Seleciona o não aluno
    #{"ra": "22222222222"}
    parceiro = Parceiro.query.filter_by(id = parceiro_id).first()

    if not parceiro:
        return jsonify({'message': 'Não encontrado!'})
    
    else:
        data = request.get_json()

        if data['ra'] is not None:
            parceiro.ra = data['ra']

        if data['nome'] is not None:
            parceiro.nome = data['nome']

        if data['email'] is not None:
            parceiro.email = data['email']

        if data['cpf'] is not None:
            parceiro.cpf = data['cpf']

        if data['senha'] is not None:
            parceiro.senha = data['senha']

        parceiro.aluno = True

        db.session.commit()

        return jsonify({'message': 'Alterado com sucesso!'})


@cp.route('/parceiro/<parceiro_id>', methods=['DELETE'])
def del_parceiro(parceiro_id):
    parceiro = Parceiro.query.filter_by(id = parceiro_id).first()

    db.session.delete(parceiro)
    db.session.commit()

    return jsonify({'message': 'Deletado com sucesso!'})

#********** Rotas do evento ********************
@cp.route('/evento', methods=['GET'])
def get_eventos():
    _atividades = Atividade.query.all()

    eventos = []

    for a in _atividades:
        ativ = {}
        ativ['titulo'] = a.titulo
        ativ['descricao'] = a.descricao
        ativ['tipo'] = a.tipo
        ativ['duracao'] = a.duracao
        ativ['banner'] = a.banner

        _eventos = Evento.query.filter_by(atividade = a.id).all()
        evento = []

        for e in _eventos:
            eve = {}
            eve['unidade'] = e.unidade
            eve['_data'] = str(e._data)
            eve['hora'] = str(e.hora)

            evento.append(eve)

        ativ['evento'] = evento
        

        _materiais  = Material.query.filter_by(atividade = a.id).all()
        mat = []
        for m in _materiais:
            material = {}
            material['material'] = m.materia
            mat.append(material)
        
        ativ['material'] = mat

        eventos.append(ativ)

    return jsonify(eventos)

@cp.route('/evento/<evento_id>', methods=['GET'])
def get_one_evento(evento_id):
    a = Atividade.query.filter_by(id = evento_id).first()

    ativ = {}
    ativ['titulo'] = a.titulo
    ativ['descricao'] = a.descricao
    ativ['tipo'] = a.tipo
    ativ['duracao'] = a.duracao
    ativ['banner'] = a.banner

    _eventos = Evento.query.filter_by(atividade = a.id).all()
    evento = []

    for e in _eventos:
        eve = {}
        eve['unidade'] = e.unidade
        eve['_data'] = str(e._data)
        eve['hora'] = str(e.hora)

        evento.append(eve)

    ativ['evento'] = evento
        

    _materiais  = Material.query.filter_by(atividade = a.id).all()
    mat = []
    for m in _materiais:
        material = {}
        material['material'] = m.materia
        mat.append(material)
        
    ativ['material'] = mat

    

    return jsonify(ativ)

@cp.route('/evento', methods=['POST'])
def post_evento():
    data = request.get_json()

    # objeto da atividade
    atividade = Atividade(
        titulo = data['titulo'], 
        descricao = data['descricao'], 
        tipo = data['tipo'], 
        duracao = data['duracao'], 
        banner = data['banner']
    )

    # objetos dos eventos
    eventos = data['eventos']

    obj_eventos = []
    for e in eventos:
        evento = Evento(
            atividade = e[0], 
            unidade = e[1], 
            _data = e[2], 
            hora = e[3]
        )
        obj_eventos.append(evento)

    # objetos dos materiais
    materiais = data['materiais']

    obj_materiais = []
    for m in materiais:
        material = Material(
            atividade = m[0],
            materia = m[1]
        )
        obj_materiais.append(material)

    # inserções no banco
    db.session.add(atividade)
    db.session.commit()

    for material in obj_materiais:
        db.session.add(material)
        db.session.commit()

    for evento in obj_eventos:
        db.session.add(evento)
        db.session.commit()
    
    return jsonify({'message': 'Cadastrado com sucesso!'})

@cp.route('/evento/<evento_id>', methods=['PUT'])
def edit_evento(evento_id):
    data = request.get_json()

    atividade = Atividade.query.filter_by(id = evento_id).first()

    atividade.titulo = data['titulo'], 
    atividade.descricao = data['descricao'], 
    atividade.tipo = data['tipo'], 
    atividade.duracao = data['duracao'], 
    atividade.banner = data['banner']

    eventos = data['eventos']

    post_evento = [e for e in eventos if not e[0]]
    put_evento = [e for e in eventos if e[0]]
    

    for e in post_evento:
        evento = Evento(
            atividade = evento_id, 
            unidade = e[1], 
            _data = e[2], 
            hora = e[3]
        )

        db.session.add(evento)  
        db.session.commit()

    for e in put_evento:
        _evento = Evento.query.filter_by(id = e[0]).first()
        
        _evento.unidade = e[1]
        _evento._data = e[2]
        _evento.hora = e[3]

        db.session.commit()

#*******************************
    materiais = data['materiais']

    post_material = [m for m in materiais if not m[0]]
    put_material = [m for m in materiais if m[0]]
    

    for m in post_material:
        material = Material(
            atividade = evento_id, 
            materia = m[1]
        )

        db.session.add(material)  
        db.session.commit()

    for m in put_material:
        _material = Material.query.filter_by(id = m[0]).first()
        
        _material.materia = m[1]

        db.session.commit()



    return jsonify({'Message': "Obrigado Senhor!"})