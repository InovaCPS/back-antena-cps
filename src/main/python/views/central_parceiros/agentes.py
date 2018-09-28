from webapp import db, cp
from models.table_parceiros import Parceiros
from models.table_agentes import Agentes
from models.table_unidades import Unidades
from models.table_atividades import Atividades
from models.table_evento import Eventos
from models.table_unidades import Unidades
from models.table_diretores import Diretores
from models.table_mensagens import Mensagens
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
        return jsonify({'Mensagem': 'Agente não encontrado!'})

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
    # if not current_user.nivel == "Administrador":
    #     return jsonify({'Mensagem': 'Você não tem Permissão'})

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
    
        return jsonify({'Mensagem': 'Cadastrado com sucesso!'})
    return jsonify({'Mensagem': 'Impossível cadastrar agente'})


@cp.route('/agentes/<int:id>', methods=['DELETE'])
@token_required
def del_agente(current_user, id):
    if not current_user.nivel == "Administrador":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'Mensagem': 'Agente não encontrado!'})

    # Quando o agente é deletado o nível da tabela de parceiros volta a ser 'Parceiro'
    parceiro = Parceiros.query.filter_by(id_geral=agente.id_parceiros).first()
    parceiro.nivel = 'Parceiro'

    db.session.delete(agente)
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso'})


@cp.route('/agentes/<int:id>', methods=['PUT'])
@token_required
def put_agente(current_user, id):
    if not current_user.nivel == "Administrador":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    agente = Agentes.query.filter_by(id=id).first()

    if not agente:
        return jsonify({'Mensagem': 'Agente não encontrado!'})

    data = request.get_json()

    parceiro = Parceiros.query.filter_by(id_geral=agente.id_parceiros).first()

    if data['matricula']:
        agente.matricula = data['matricula']

    if data['hora']:
        agente.hora = data['hora']
    
    if data['id_unidade']:
        agente.id_unidade = ['id_unidade']

    db.session.commit()

    return redirect(url_for('.edit_parceiro', parceiro_id=parceiro.id_geral), code=307)

@cp.route('/agentes/atividades', methods=['GET'])
@token_required
def get_ativ_agente(current_user):
    if not current_user.nivel == "Agente":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    agente = Agentes.query.filter_by(id_parceiros=current_user.id_geral).first()
    atividades = Atividades.query.filter_by(id_agente=agente.id).all()

    eventos = []

    for a in atividades:
        if not a.id_eixo:
            ativ = {}
            ativ['id'] = a.id
            ativ['titulo'] = a.titulo
            ativ['tipo'] = a.tipo

            eventos.append(ativ)

    return jsonify(eventos)

@cp.route('/agentes/atividades/<int:id>', methods=['GET', 'PUT'])
@token_required
def get_one_ativ_agente(current_user, id):
    if not current_user.nivel == "Agente":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    if request.method == 'GET':

        atividade = Atividades.query.filter_by(id=id).first()
        agente = Agentes.query.filter_by(id_parceiros=current_user.id_geral).first()

        if atividade.id_agente == agente.id:
            return redirect(url_for('.get_one_evento', id=id), code=307)
        else:
            return jsonify({'Mensagem': 'Este evento não foi atribuído a você!'})

    else:
        data = request.get_json()

        atividade = Atividades.query.filter_by(id = id).first()

        atividade.id_eixo = data['eixo']

        db.session.commit()

        eventos = Eventos.query.filter_by(id_atividades=atividade.id).all()

        for evento in eventos:
            evento.situacao = 'Aguardando resposta do diretor'
            db.session.commit()
            unidade = Unidades.query.filter_by(id=evento.id_unidades).first()
            diretor = Diretores.query.filter_by(id_unidades=unidade.id).first()

            mensagem = Mensagens(
                'Há um(a) novo(a) pedido de evento na sua unidade para avaliação', 
                False, 
                atividade.id_parceiro, 
                diretor.id_parceiros
            )

            db.session.add(mensagem)
            db.session.commit()

        return jsonify({'Mensagem': 'Eixo do evento alterado!'})