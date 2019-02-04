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

@cp.route('/aluno/<int:id>', methods=['GET'])
@token_required
def get_one_aluno(current_user, id):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    diretor = Diretores.query.filter_by(id_parceiros=current_user.id_geral).first()
    aluno = Alunos.query.filter_by(id_unidades=diretor.id_unidades, id_parceiros=id).first()

    if not aluno:
        return jsonify({'Mensagem': 'O ID informado é inválido!'})

    parceiro = Parceiros.query.filter_by(id_geral = id).first()
    unidade = Unidades.query.filter_by(id=aluno.id_unidades).first()

    info = {}
    info['nome'] = parceiro.nome
    info['sobrenome'] = parceiro.sobrenome
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
    info['escola'] = unidade.nome
    info['escola_cidade'] = unidade.cidade

    return jsonify(info)

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