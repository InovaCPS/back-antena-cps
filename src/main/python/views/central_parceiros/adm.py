from webapp import db, cp
from models.table_parceiros import Parceiros
from flask import request, jsonify, url_for
from views.central_parceiros.login import token_required

@cp.route('/adm', methods=['POST', 'DELETE'])
@token_required
def admin(current_user):
    permissoes = ['Mestre']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    if request.method == 'POST':
        dados = request.get_json()

        parceiro = Parceiros.query.filter_by(id_geral=dados['id']).first()

        if not parceiro:
            return jsonify({'Mensagem': 'Parceiro não encontrado!'})

        parceiro.nivel = 'Administrador'
        db.session.commit()

        return jsonify({'Mensagem': 'Administrador cadastrado'})
    
    else:
        dados = request.get_json()

        parceiro = Parceiros.query.filter_by(id_geral=dados['id']).first()

        if not parceiro:
            return jsonify({'Mensagem': 'Parceiro não encontrado!'})

        if not parceiro.nivel == 'Administrador':
            return jsonify({'Mensagem': 'O parceiro informado não é administrador!'})

        parceiro.nivel = 'Parceiro'
        db.session.commit()

        return jsonify({'Mensagem': 'Administrador deletado'})