from webapp import db, cp
from models.table_parceiros import Parceiros
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from views.central_parceiros.login import token_required


@cp.route('/parceiro', methods=['GET'])
@token_required
def get_parceiro(current_user):
    dados = Parceiros.query.all()

    parceiros = []

    for info in dados:
        parceiro = {}
        parceiro['id_geral'] = info.id_geral
        parceiro['nivel'] = info.nivel
        parceiro['nome'] = info.nome
        parceiro['sobrenome'] = info.sobrenome
        parceiro['email'] = info.email
        parceiro['cpf'] = info.cpf
        parceiro['dt_nascimento'] = str(info.dt_nascimento)
        parceiro['genero'] = info.genero
        parceiro['telefone'] = info.telefone 
        parceiro['local_trabalho'] = info.local_trabalho
        parceiro['cargo'] = info.cargo
        parceiro['lattes'] = info.lattes
        parceiro['facebook']= info.facebook
        parceiro['linkedin'] = info.linkedin 
        parceiro['twitter'] = info.twitter

        parceiros.append(parceiro)

    return jsonify(parceiros)


@cp.route('/parceiro/<parceiro_id>', methods=['GET'])
@token_required
def get_one_parceiro(current_user, parceiro_id):
    info = Parceiros.query.filter_by(id_geral=parceiro_id).first()

    if not info:
        return jsonify({'Mensagem': 'Não encontrado!'})

    parceiro = {}
    parceiro['id_geral'] = info.id_geral
    parceiro['nivel'] = info.nivel
    parceiro['nome'] = info.nome
    parceiro['sobrenome'] = info.sobrenome
    parceiro['email'] = info.email
    parceiro['cpf'] = info.cpf
    parceiro['dt_nascimento'] = str(info.dt_nascimento)
    parceiro['genero'] = info.genero
    parceiro['telefone'] = info.telefone
    parceiro['local_trabalho'] = info.local_trabalho
    parceiro['cargo'] = info.cargo
    parceiro['lattes'] = info.lattes
    parceiro['facebook']= info.facebook
    parceiro['linkedin'] = info.linkedin 
    parceiro['twitter'] = info.twitter

    return jsonify(parceiro)


@cp.route('/parceiro', methods=['POST'])
def post_parceiro():
    data = request.get_json()
    password = generate_password_hash(data['senha'])

    parceiro = Parceiros(
        nivel='Parceiro',
        nome=data['nome'],
        sobrenome=data['sobrenome'],
        email=data['email'],
        senha=password
        )
    

    db.session.add(parceiro)
    db.session.commit()

    return jsonify({'Mensagem': 'Adicionado com sucesso!'})


@cp.route('/parceiro/<parceiro_id>', methods=['PUT'])
@token_required
def edit_parceiro(current_user, parceiro_id):
    parceiro = Parceiros.query.filter_by(id_geral=parceiro_id).first()

    if not parceiro:
        return jsonify({'Mensagem': 'Não encontrado!'})

    else:
        data = request.get_json()

        if data['nome']:
            parceiro.nome = data['nome']

        if data['sobrenome']:
            parceiro.sobrenome = data['sobrenome']

        if data['email']:
            parceiro.email = data['email']

        if data['cpf']:
            parceiro.cpf = data['cpf']

        if data['senha']:
            senha = generate_password_hash(data['senha'])
            parceiro.senha = senha

        if data['rg']:
            parceiro.rg = data['rg']

        if data['dt_nascimento']:
            parceiro.dt_nascimento = data['dt_nascimento']

        if data['genero']:
            parceiro.genero = data['genero']

        if data['telefone']:
            parceiro.telefone = data['telefone']

        if data['local_trabalho']:
            parceiro.local_trabalho = data['local_trabalho']
        
        if data['cargo']:
            parceiro.cargo = data['cargo']

        if data['lattes']:
            parceiro.lattes = data['lattes']

        if data['facebook']:
            parceiro.facebook = data['facebook']

        if data['linkedin']:
            parceiro.linkedin = data['linkedin']

        if data['twitter']:
            parceiro.twitter = data['twitter']

        db.session.commit()

        return jsonify({'Mensagem': 'Alterado com sucesso!'})


@cp.route('/parceiro/<parceiro_id>', methods=['DELETE'])
@token_required
def del_parceiro(current_user, parceiro_id):
    parceiro = Parceiros.query.filter_by(id_geral=parceiro_id).first()
    inscricao = Inscricoes.query.filter_by(id_parceiros = parceiro_id).first()

    if parceiro.nivel == "Aluno":
        aluno = Alunos.query.filter_by(id_parceiros = parceiro.id_geral).first()

        db.session.delete(aluno)
        db.session.commit()

    elif parceiro.nivel == "Diretor":
        diretor = Diretores.query.filter_by(id_parceiros = parceiro.id_geral).first()
        mensagem = Mensagens.query.filter_by(id_destinatario = diretor.id).first()

        db.session.delete(mensagem)
        db.session.commit()
        
        db.session.delete(diretor)
        db.session.commit()

    elif parceiro.nivel == 'Agente':
        agente = Agentes.query.filter_by(id_parceiros = parceiro.id_geral).first()

        mensagem = Mensagens.query.filter_by(id_destinatarios = parceiro.id_geral).first()

        atividades = Atividades.query.filter_by(id_agente = agente.id).first()

        if not atividades and not mensagem:

            db.session.delete(agente)
            db.session.commit()

        else:
            return jsonify({'Mensagem': 'Você tem algumas atividades pendentes!'})

    db.session.delete(inscricao)
    db.session.commit()
    
    db.session.delete(parceiro)
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso!'})