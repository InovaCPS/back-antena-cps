from webapp import db, cp
from models.table_mensagens import Mensagens
from flask import request, jsonify, redirect, url_for
from views.central_parceiros.login import token_required


@cp.route('/mensagem', methods=['GET'])
@token_required
def get_message(current_user):

    msg = Mensagens.query.filter_by(id_destinatarios = int(current_user.id_geral)).all()

    if not msg:
        return jsonify({'Mensagem': 'Nenhuma notificação!'})

    mensagens = []

    for m in msg:
        mensagem = {}
        mensagem['id'] = m.id
        mensagem['descricao'] = m.descricao

        mensagens.append(mensagem)

    return jsonify(mensagens)