from webapp import cp, db
from models.table_alunos import Alunos
from models.table_parceiros import Parceiros
from models.table_diretores import Diretores
from models.table_unidades import Unidades
from views.central_parceiros.login import token_required
from flask import jsonify, request, redirect, url_for

@cp.route('/aluno', methods=['GET'])
@token_required
def get_alunos(current_user):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    alunos = Alunos.query.filter_by(id_unidades=diretor.id_unidades).all()

    _alunos = []
    for aluno in alunos:
        parceiro = Parceiros.query.filter_by(id_geral = aluno.id_parceiros).first()

        info = {}
        info['nome'] = parceiro.nome
        info['ra'] = aluno.ra

        _alunos.append(info)

    return jsonify(_alunos)

@cp.route('/aluno/<int:ra>', methods=['GET'])
@token_required
def get_one_aluno(current_user, ra):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    aluno = Alunos.query.filter_by(id_unidades=diretor.id_unidades, ra=ra).first()

    if not aluno:
        return jsonify({'Mensagem': 'O RA informado é inválido!'})

    parceiro = Parceiros.query.filter_by(id_geral = aluno.id_parceiros).first()

    info = {}
    info['nome'] = parceiro.nome
    info['ra'] = aluno.ra
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
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    unidade = Unidades.query.filter_by(id=diretor.id_unidades).first()
    
    parceiro = Parceiros.query.filter_by(id_geral = current_user.id_geral).first()
    aluno = Alunos.query.filter_by(id_parceiros=current_user.id_geral).first()

    if aluno:
        return jsonify({'Mensagem': 'O usuário já está cadastrado como aluno!'})

    aluno = Alunos(data['ra'], unidade.id, data['id_parceiro'])    
    db.session.add(aluno)
    db.session.commit()
    
    parceiro_aluno = Parceiros.query.filter_by(id_geral=aluno.id_parceiros).first()
    parceiro_aluno.nivel = "Aluno"
    db.session.commit()

    return jsonify({'Mensagem': 'Cadastrado com sucesso!'})

@cp.route('/aluno/<int:ra>', methods=['PUT'])
@token_required
def edit_aluno(current_user, ra):
    if not current_user.nivel == "Diretor":
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()

    aluno = Alunos.query.filter_by(ra=ra).first()

    if not aluno:
        return jsonify({'Mensagem': 'Aluno não encontrado!'})
    else:

        aluno.ra = data['ra']
        db.session.commit()
        
        return jsonify({'Mensagem': 'RA alterado com sucesso!'})

@cp.route('/aluno/<int:ra>', methods=['DELETE'])
@token_required
def del_aluno(current_user, ra):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    aluno = Alunos.query.filter_by(id_unidades=diretor.id_unidades, ra=ra).first()

    if not aluno:
        return jsonify({'Mensagem': 'O RA informado é inválido!'})

    parceiro_aluno = Parceiros.query.filter_by(id_geral=aluno.id_parceiros).first()
        
    db.session.delete(aluno)
    db.session.commit()

    parceiro_aluno.nivel = 'Parceiro'
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso!'})