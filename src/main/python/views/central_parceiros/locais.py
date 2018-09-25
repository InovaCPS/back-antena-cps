from flask import jsonify
from webapp import db, cp
from models.table_regioes import Regioes
from models.table_unidades import Unidades

@cp.route('/locais', methods=['GET'])
def get_locais():
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