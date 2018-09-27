from webapp import cp, db
from models.table_parceiros import Parceiros
from models.table_diretores import Diretores
from models.table_unidades import Unidades
from models.table_regioes import Regioes
from models.table_evento import Eventos
from models.table_atividades import Atividades
from flask import request, jsonify, redirect, url_for
from views.central_parceiros.login import token_required


@cp.route('/diretores', methods=['GET'])
def get_diretores():
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretores = Diretores.query.all()

    info = []

    for diretor in diretores:
        unidade = Unidades.query.filter_by(id = diretor.id_unidades).first()
        parceiro = Parceiros.query.filter_by(id_geral = diretor.id_parceiros).first()

        dado_diretor = {}
        dado_diretor['id'] = diretor.id
        dado_diretor['nome'] = parceiro.nome
        dado_diretor['email'] = parceiro.email
        dado_diretor['unidade'] = unidade.nome
        dado_diretor['endereco'] = unidade.endereco

        info.append(dado_diretor)

    return jsonify(info)

@cp.route('/diretores/<id_diretor>', methods=['GET'])
def get_one_diretor(id_diretor):
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id = id_diretor).first()
    
    if not diretor:
        return jsonify({'Mensagem': 'Diretor não encontrado'})
    else:
        unidade = Unidades.query.filter_by(id = diretor.id_unidades).first()
        regiao = Regioes.query.filter_by(id = unidade.id_regioes).first()
        parceiro = Parceiros.query.filter_by(id_geral = diretor.id_parceiros).first()

        dado_diretor = {}
        dado_diretor['id'] = diretor.id
        dado_diretor['nome'] = parceiro.nome
        dado_diretor['email'] = parceiro.email
        dado_diretor['cpf'] = parceiro.cpf
        dado_diretor['rg'] = parceiro.rg
        dado_diretor['dt_nascimento'] = str(parceiro.dt_nascimento)
        dado_diretor['genero'] = parceiro.genero        
        dado_diretor['telefone'] = parceiro.telefone

        instituicao = {}
        instituicao['unidade'] = unidade.nome
        instituicao['endereco'] = unidade.endereco
        instituicao['regiao'] = regiao.nome
        dado_diretor['diretor'] = instituicao


        local = {}
        local['local_trabalho'] = parceiro.local_trabalho
        local['cargo'] = parceiro.cargo
        dado_diretor['trabalho'] = local

        social = {}
        social['lattes'] = parceiro.lattes
        social['facebook'] = parceiro.facebook
        social['linkedin'] = parceiro.linkedin
        social['twitter'] = parceiro.twitter
        dado_diretor['redes sociais'] = social

     

        return jsonify(dado_diretor)

@cp.route('/diretores', methods=['POST'])
def post_diretor():
    if not current_user.nivel == "Administrador":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()

    parceiro = Parceiros.query.filter_by(id_geral = data['id_parceiros']).first()

    if parceiro is not None and parceiro.nivel == 'Parceiro':

        diretor = Diretores(id_unidades = data['id_unidades'], id_parceiros = data['id_parceiros'])

        parceiro.nivel = "Diretor"
        
        db.session.add(diretor)
        db.session.commit()

        return jsonify({'Mensagem': 'Diretor cadastrado com sucesso!'})

    return jsonify({'Mensagem': 'Impossível cadastrar diretor!'})


@cp.route('/diretores/<id_diretor>', methods=['PUT'])
def edit_diretor(id_diretor):
    if not current_user.nivel == "Administrador":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id = id_diretor).first()

    if not diretor:
        return jsonify({'Mensagem': 'Diretor não encontrado!'})
    else:
        return redirect(url_for('.edit_parceiro', parceiro_id=diretor.id_parceiros), code=307)


@cp.route('/diretores/atividades', methods=['GET'])
@token_required
def get_evento_diretor(current_user):
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first() # retorna o diretor que está logado
    unidade = Unidades.query.filter_by(id=diretor.id_unidades).first() # retorna a unidade da qual ele é diretor
    eventos = Eventos.query.filter_by(id_unidades=unidade.id).all() # retorna os pedidos de evento daquela unidade

    eventos_ = []

    for evento in eventos:
        atividade = Atividades.query.filter_by(id=evento.id_atividades).first()

        ev = {}
        ev['titulo'] = atividade.titulo
        ev['descricao'] = atividade.descricao
        ev['tipo'] = atividade.tipo
        ev['data'] = evento._data
        ev['hora'] = str(evento.hora)
        ev['id_evento'] = evento.id

        eventos_.append(ev)

    return jsonify(eventos_)

@cp.route('/diretores/atividades/<int:id>', methods=['GET', 'PUT'])
@token_required
def get_one_evento_diretor(current_user, id):
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()

    evento = Eventos.query.filter_by(id=id).first()
    if request.method == 'GET':
        atividade = Atividades.query.filter_by(id=evento.id_atividades).first()
        parceiro = Parceiros.query.filter_by(id_geral=atividade.id_parceiro).first()

        ev = {}
        ev['titulo'] = atividade.titulo
        ev['descricao'] = atividade.descricao
        ev['tipo'] = atividade.tipo
        ev['duracao'] = atividade.duracao
        ev['banner'] = atividade.banner
        ev['parceiro'] = parceiro.nome
        ev['email'] = parceiro.email
        ev['telefone'] = parceiro.telefone
        ev['cargo_parceiro'] = parceiro.cargo
        ev['local_trabalho_parceiro'] = parceiro.local_trabalho
        ev['data'] = evento._data
        ev['hora'] = str(evento.hora)

        return jsonify(ev)
    else:
        data = request.get_json()

        evento.situacao = data['resposta']

        db.session.commit()

        return jsonify({'Mensagem': 'Resposta cadastrada!'})