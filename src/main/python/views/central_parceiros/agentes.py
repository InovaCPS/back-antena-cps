from webapp import db, cp
from models.table_parceiros import Parceiros
from models.table_agentes import Agentes
from models.table_unidades import Unidades
from flask import request, jsonify, redirect, url_for
from views.central_parceiros.login import token_required


@cp.route('/agentes', methods=['GET'])
def get_agentes():
    dados = Agentes.query.all()

    agentes = []

    for a in dados:
        unidade = Unidades.query.filter_by(id=a.id_unidades).first()
        parceiro = Parceiros.query.filter_by(id_geral=a.id_parceiros).first()

        agente = {}
        agente['nome'] = parceiro.nome
        agente['email'] = parceiro.email
        agente['telefone'] = parceiro.telefone
        agente['cpf'] = parceiro.cpf
        agente['matricula'] = a.matricula
        agente['hora'] = a.hora
        agente['unidade'] = unidade.nome
        agente['endereço'] = unidade.endereco

        agentes.append(agente)

    return jsonify(agentes)


@cp.route('/agentes/<int:id>', methods=['GET'])
def get_agente(id):
    a = Agentes.query.filter_by(id=id).first()
    if not a:
        return jsonify({'Message': 'Agente não encontrado!'})

    unidade = Unidades.query.filter_by(id=a.id_unidades).first()
    parceiro = Parceiros.query.filter_by(id_geral=a.id_parceiros).first()

    agente = {}
    agente['nome'] = parceiro.nome
    agente['email'] = parceiro.email
    agente['telefone'] = parceiro.telefone
    agente['cpf'] = parceiro.cpf
    agente['matricula'] = a.matricula
    agente['hora'] = a.hora
    agente['unidade'] = unidade.nome
    agente['endereço'] = unidade.endereco

    return jsonify(agente)


@cp.route('/agentes', methods=['POST'])
@token_required
def post_agente(current_user):
    data = request.get_json()

    parceiro = Parceiros.query.filter_by(id_geral=data['id_parceiro']).first()

    if parceiro is not None and parceiro.nivel == 'Parceiro':

        agente = Agentes(
            matricula = data['matricula'], 
            hora = data['hora'], 
            id_unidades = data['id_unidade'], 
            id_parceiros = data['id_parceiro']
        )

        db.session.add(agente)

        parceiro.nivel = 'Agente'

        db.session.commit()
    
        return jsonify({'message': 'Cadastrado com sucesso!'})
    return jsonify({'message': 'Impossível cadastrar agente'})


@cp.route('/agentes/<int:id>', methods=['DELETE'])
@token_required
def del_agente(current_user, id):
    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'message': 'Agente não encontrado!'})

    # Quando o agente é deletado o nível da tabela de parceiros volta a ser 'Parceiro'
    parceiro = Parceiros.query.filter_by(id_geral=agente.id_parceiros).first()
    parceiro.nivel = 'Parceiro'

    db.session.delete(agente)
    db.session.commit()

    return jsonify({'message': 'Deletado com sucesso'})


@cp.route('/agentes/<int:id>', methods=['PUT'])
@token_required
def put_agente(current_user, id):
    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'message': 'Agente não encontrado!'})

    data = request.get_json()

    parceiro = Parceiros.query.filter_by(id_geral=agente.id_parceiros).first()

    if data['matricula']:
        agente.matricula = data['matricula']

    if data['hora']:
        agente.hora = data['hora']
    
    if data['id_unidade']:
        agente.id_unidade = ['id_unidade']

    db.session.commit()

    # Ao atualizar as informações pertencentes apenas a tabela de agentes
    # o restante das informações é atualizado no método de atualizar parceiros
    # para evitar código duplicado
    # O código 307 é para o redirect não ser tratado como GET 
    # e conseguir fazer as alterações
    return redirect(url_for('.edit_parceiro', parceiro_id=parceiro.id_geral), code=307)