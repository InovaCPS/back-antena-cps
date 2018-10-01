from webapp import cp, db
from models.table_alunos import Alunos
from models.table_parceiros import Parceiros
from views.central_parceiros.login import token_required
from flask import jsonify, request, redirect, url_for

@cp.route('/aluno', methods=['GET'])
@token_required
def get_one_aluno(current_user):
    aluno = Alunos.query.filter_by(id_parceiros = current_user.id_geral).first()

    if not aluno:
        return jsonify({'Mensagem': 'Aluno não encontrado!'})

    parceiro = Parceiros.query.filter_by(id_geral = current_user.id_geral).first()

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

    return jsonify(info)

@cp.route('/aluno', methods=['POST'])
@token_required
def create_aluno(current_user):
    data = request.get_json()
    
    parceiro = Parceiros.query.filter_by(id_geral = current_user.id_geral).first()

    aluno = Alunos(data['ra'], data['local_estudo'], current_user.id_geral)    
    db.session.add(aluno)
    db.session.commit()
    
    parceiro.nivel = "aluno"
    db.session.commit()

    return jsonify({'Mensagem': 'Agora Você é um aluno!'})

@cp.route('/aluno', methods=['PUT'])
@token_required
def edit_aluno(current_user):
    aluno = Alunos.query.filter_by(id_parceiros = current_user.id_geral).first()

    if not aluno:
        return jsonify({'Mensagem': 'Aluno não encontrado!'})

    else:
        return redirect(url_for('.edit_parceiro', parceiro_id = aluno.id_parceiros), code=307)
    return ''

@cp.route('/aluno/<ra>', methods=['DELETE'])
@token_required
def del_aluno(current_user, ra):
    aluno = Alunos.query.filter_by(ra = ra).first()
    db.session.delete(aluno)
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso!'})