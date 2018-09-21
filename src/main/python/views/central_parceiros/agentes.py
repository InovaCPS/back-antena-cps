from webapp import app, db, cp
from models.table_parceiros import Parceiros
from models.table_atividades import Atividades
from models.table_material import Materiais
from models.table_agentes import Agentes
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


@cp.route('/agentes', methods=['GET'])
def get_agentes():
    dados = Agentes.query.all()

    agentes = []

    for info in dados:
        agente = {}
        #arrumar
        agente['matricula'] = info.matricula
        agente['nome'] = info.nome
        agente['rg'] = info.rg
        agente['cpf'] = info.cpf
        agente['cargo'] = info.cargo
        agente['unidade'] = info.unidade
        agente['haeo'] = info.haeo
        agente['lattes'] = info.lattes
        agente['regiao'] = info.regiao

        agentes.append(agente)

    return jsonify(agentes)


@cp.route('/agentes/<int:id>', methods=['GET'])
def get_agente():
    a = Agentes.query.filter_by(id=id).first()
    if not a:
        return jsonify({'Message': 'Agente não encontrado!'})

    agente = {}
    #arrumar
    agente['nome'] = info.nome
    agente['rg'] = info.rg
    agente['cpf'] = info.cpf
    agente['cargo'] = info.cargo
    agente['unidade'] = info.unidade
    agente['haeo'] = info.haeo
    agente['lattes'] = info.lattes
    agente['regiao'] = info.regiao

    return jsonify(agente)


@cp.route('/agentes', methods=['POST'])
def post_agente():
    data = request.get_json()

    agente = Agentes(
        nome = data['nome'],
        rg = data['rg'],
        cpf = data['cpf'],
        cargo = data['cargo'],
        unidade = data['unidade'],
        haeo = data['haeo'],
        lattes = data['lattes'],
        regiao = data['regiao']
    )

    db.session.add(agente)
    db.session.commit()

    return jsonify({'message': 'Cadastrado com sucesso!'})


@cp.route('/agentes/<int:id>', methods=['DELETE'])
def del_agente():
    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'message': 'Agente não encontrado!'})

    db.session.delete(agente)
    db.session.commit()

    return jsonify({'message': 'Deletado com sucesso'})


@cp.route('/agentes/<int:id>', methods=['PUT'])
def put_agente():
    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'message': 'Agente não encontrado!'})

    else:
        data = request.get_json()

        if data['nome']:
            agente.nome = data['nome']

        if data['rg']:
            agente.rg = data['rg']

        if data['cpf']:
            agente.cpf = data['cpf']

        if data['cargo']:
            agente.cargo = data['cargo']

        if data['unidade']:
            agente.unidade = data['unidade']

        if data['haeo']:
            agente.haeo = data['haeo']

        if data['lattes']:
            agente.lattes = data['lattes']

        if data['regiao']:
            agente.regiao = data['regiao']

        db.session.commit()

        return jsonify({'message': 'Alterado com sucesso!'})