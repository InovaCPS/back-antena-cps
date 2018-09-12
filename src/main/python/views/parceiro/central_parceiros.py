from webapp import app, db
from models.parceiro import Parceiro
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

cp = Blueprint('cp', __name__)

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
