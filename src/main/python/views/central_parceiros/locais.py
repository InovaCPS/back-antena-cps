from flask import jsonify
from webapp import db, cp
from models.table_regioes import Regioes
from models.table_unidades import Unidades
from views.central_parceiros.login import token_required

@cp.route('/locais', methods=['GET'])
@token_required
def get_locais(current_user):
    regioes = Regioes.query.all()
    unidades = Unidades.query.all()

    locais = []

    for regiao in regioes:
        unidades_da_regiao = [u for u in unidades if u.id_regioes == regiao.id]

        local = {}
        local['id_regiao'] = regiao.id
        local['regiao'] = regiao.nome        

        unidade_ = []

        for unidade in unidades_da_regiao:
            u = {}
            u['nome'] = unidade.nome
            u['endereco'] = unidade.endereco
            u['id_unidade'] = unidade.id

            unidade_.append(u)

        local['unidades'] = unidade_

        locais.append(local)

    return jsonify(locais)

@cp.route('/unidades', methods=['GET'])
@token_required
def get_unidades(current_user):
    unidades = Unidades.query.all()

    lista_unidades = []

    for unidade in unidades:
        u = {}
        
        u['id'] = unidade.id
        u['nome'] = unidade.nome
        u['endereco'] = unidade.endereco
        u['bairro'] = unidade.bairro
        u['cidade'] = unidade.cidade
        u['id_regiao'] = unidade.id_regioes

        lista_unidades.append(u)
    
    return jsonify(lista_unidades)