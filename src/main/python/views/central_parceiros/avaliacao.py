from webapp import db, cp
from models.table_avaliacoes import Avaliacoes
from flask import jsonify

def avaliar(data, tipo, avaliado, avaliador):
    try:
        if float(data['nota']) < 1 or float(data['nota']) > 5:
            nota = data['nota']
        else:
            return jsonify({'Mensagem': 'A nota enviada precisa ser entre 1 e 5'})

        avaliacao = Avaliacoes(
            id_evento = evento_id, 
            tipo_avaliado = tipo,
            id_avaliado = avaliado,
            id_avaliador = avaliador, 
            nota = float(data['nota']), 
            comentario = data['comentario'], 
            identificar = data['identificar']
        )

        db.session.add(avaliacao)
        db.session.commit()
        return jsonify({'Mensagem': '{} avaliado com sucesso!'.format(tipo)})

    except ValueError:
        return jsonify({'Mensagem': 'A nota precisa ser um valor numérico!'})
