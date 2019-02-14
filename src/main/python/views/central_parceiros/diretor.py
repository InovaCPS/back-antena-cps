from webapp import cp, db
from models.table_parceiros import Parceiros
from models.table_alunos import Alunos
from models.table_diretores import Diretores
from models.table_unidades import Unidades
from models.table_regioes import Regioes
from models.table_evento import Eventos
from models.table_atividades import Atividades
from flask import request, jsonify, redirect, url_for
from views.central_parceiros.login import token_required


@cp.route('/diretores', methods=['GET'])
@token_required
def get_diretores(current_user):
    permissoes = ['Diretor', 'Administrador', 'Mestre']
    if not current_user.nivel in permissoes:
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
@token_required
def get_one_diretor(current_user, id_diretor):
    permissoes = ['Diretor', 'Administrador', 'Mestre']
    if not current_user.nivel in permissoes:
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
@token_required
def post_diretor(current_user):
    permissoes = ['Administrador', 'Mestre']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()

    parceiro = Parceiros.query.filter_by(id_geral = data['id_parceiro']).first()

    if parceiro is not None and parceiro.nivel == 'Parceiro':
        unidade = Unidades.query.filter_by(id=data['id_unidade']).first()
        if not unidade:
            return jsonify({'Mensagem': 'Unidade não encontrada!'})

        diretor = Diretores(id_unidades = data['id_unidade'], id_parceiros = data['id_parceiro'])

        parceiro.nivel = "Diretor"
        
        db.session.add(diretor)
        db.session.commit()

        return jsonify({'Mensagem': 'Diretor cadastrado com sucesso!'})

    return jsonify({'Mensagem': 'Impossível cadastrar diretor!'})


@cp.route('/diretores/<id_diretor>', methods=['PUT'])
@token_required
def edit_diretor(current_user, id_diretor):
    permissoes = ['Administrador', 'Mestre', 'Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id = id_diretor).first()

    if not diretor:
        return jsonify({'Mensagem': 'Diretor não encontrado!'})
    else:
        return redirect(url_for('.edit_parceiro', parceiro_id=diretor.id_parceiros), code=307)

@cp.route('/diretores/<int:id>', methods=['DELETE'])
@token_required
def del_diretor(current_user, id):
    permissoes = ['Administrador', 'Mestre']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id = id).first()

    if not diretor:
        return jsonify({'Mensagem': 'Diretor não encontrado!'})
    else:
        db.session.delete(diretor)

        return jsonify({'Mensagem': 'Diretor apagado com sucesso!'})

@cp.route('/diretores/atividades', methods=['GET'])
@token_required
def get_evento_diretor(current_user):
    permissoes = ['Diretor', 'Mestre']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    if current_user.nivel == 'Diretor':
        diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first() # retorna o diretor que está logado
        unidade = Unidades.query.filter_by(id=diretor.id_unidades).first() # retorna a unidade da qual ele é diretor
        eventos = Eventos.query.filter_by(id_unidades=unidade.id).all() # retorna os pedidos de evento daquela unidade
    else:
        eventos = Eventos.query.all()

    eventos_ = []

    for evento in eventos:
        # melhor ideia no momento, pode ser melhorado
        if evento.situacao == 'Aguardando resposta do diretor':
            atividade = Atividades.query.filter_by(id=evento.id_atividades).first()

            ev = {}
            ev['titulo'] = atividade.titulo
            ev['tipo'] = atividade.tipo
            ev['data'] = evento._data.strftime('%d/%m/%Y')
            ev['hora'] = str(evento.hora)
            ev['id_evento'] = evento.id

            eventos_.append(ev)

    return jsonify(eventos_)

@cp.route('/diretores/atividades/<int:id>', methods=['GET', 'PUT'])
@token_required
def get_one_evento_diretor(current_user, id):
    permissoes = ['Diretor', 'Mestre']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    evento = Eventos.query.filter_by(id=id).first()
    if not evento:
        return jsonify({'Mensagem': 'Evento não encontrado'})

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
        ev['data'] = evento._data.strftime('%d/%m/%Y')
        ev['hora'] = str(evento.hora)

        return jsonify(ev)
    else:
        data = request.get_json()

        if data['resposta'] == True:
            evento.situacao = 'Aprovado'
            evento.capacidade = data['capacidade']
            evento.inscrito = 0
        else:
            evento.situacao = 'Recusado'

        db.session.commit()

        return jsonify({'Mensagem': 'Resposta cadastrada!'})

@cp.route('/diretores/alunos', methods=['GET'])
@token_required
def get_alunos_unidade(current_user):
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    alunos = Alunos.query.filter_by(id_unidades=diretor.id_unidades).all()

    _alunos = []

    for aluno in alunos:
        parceiro = Parceiros.query.filter_by(id_geral=aluno.id_parceiros).first()

        info = {}
        info['nome'] = parceiro.nome
        info['nivel'] = parceiro.nivel
        info['ra'] = aluno.ra
        info['email'] = parceiro.email
        info['email'] = parceiro.email
        info['cpf'] = parceiro.cpf
        info['dt_nascimento'] = str(parceiro.dt_nascimento)
        info['genero'] = parceiro.genero
        info['telefone'] = parceiro.telefone 
        info['local_trabalho'] = parceiro.local_trabalho
        info['cargo'] = parceiro.cargo
        info['lattes'] = parceiro.lattes
        info['facebook']= parceiro.facebook
        info['linkedin'] = parceiro.linkedin 
        info['twitter'] = parceiro.twitter

        _alunos.append(info)

    return jsonify(_alunos)