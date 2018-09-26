from webapp import cp, db
from models.table_parceiros import Parceiros
from models.table_diretores import Diretores
from models.table_unidades import Unidades
from models.table_regioes import Regioes
from flask import request, jsonify, redirect, url_for



@cp.route('/diretores', methods=['GET'])
def get_diretores():
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
    diretor = Diretores.query.filter_by(id = id_diretor).first()

    if not diretor:
        return jsonify({'Mensagem': 'Diretor não encontrado!'})
    else:
        return redirect(url_for('.edit_parceiro', parceiro_id=diretor.id_parceiros), code=307)