from datetime import date
from webapp import db, cp, mail
from models.table_parceiros import Parceiros
from models.table_inscricoes import Inscricoes
from models.table_alunos import Alunos
from models.table_agentes import Agentes
from models.table_diretores import Diretores
from models.table_atividades import Atividades
from models.table_mensagens import Mensagens
from models.table_avaliacoes import Avaliacoes
from flask import request, jsonify, url_for
from werkzeug.security import generate_password_hash
from views.central_parceiros.login import token_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from sqlalchemy import exc

s = URLSafeTimedSerializer('this-is-secret') #melhorar essa chave de segurança

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@cp.route('/getId', methods=['GET'])
@token_required
def getId(current_user):
    infos = {}
    infos['id'] = current_user.id_geral
    infos['nivel'] = current_user.nivel

    return jsonify(infos)

@cp.route('/parceiro', methods=['GET'])
@token_required
def get_parceiro(current_user):
    dados = Parceiros.query.all()

    parceiros = []

    for info in dados:
        parceiro = {}
        parceiro['id_geral'] = info.id_geral
        parceiro['nivel'] = info.nivel
        parceiro['nome'] = info.nome
        parceiro['sobrenome'] = info.sobrenome
        parceiro['email'] = info.email

        parceiros.append(parceiro)

    return jsonify(parceiros)


@cp.route('/parceiro/<parceiro_id>', methods=['GET'])
@token_required
def get_one_parceiro(current_user, parceiro_id):
    info = Parceiros.query.filter_by(id_geral=parceiro_id).first()

    if not info:
        return jsonify({'Mensagem': 'Não encontrado!'})

    parceiro = {}
    parceiro['id_geral'] = info.id_geral
    parceiro['nivel'] = info.nivel
    parceiro['nome'] = info.nome
    parceiro['sobrenome'] = info.sobrenome
    parceiro['email'] = info.email
    parceiro['cpf'] = info.cpf
    parceiro['rg'] = info.rg
    parceiro['foto_perfil'] = info.foto_perfil
    parceiro['dt_nascimento'] = str(info.dt_nascimento)
    parceiro['genero'] = info.genero
    parceiro['telefone'] = info.telefone
    parceiro['local_trabalho'] = info.local_trabalho
    parceiro['cargo'] = info.cargo
    parceiro['lattes'] = info.lattes
    parceiro['facebook']= info.facebook
    parceiro['linkedin'] = info.linkedin 
    parceiro['twitter'] = info.twitter
    parceiro['idade'] = ""

    if info.dt_nascimento:
        parceiro['idade'] = calculate_age(info.dt_nascimento)
        

    return jsonify(parceiro)


@cp.route('/parceiro', methods=['POST'])
def post_parceiro():
    data = request.get_json()
    password = generate_password_hash(data['senha'])

    parceiro = Parceiros(
        nivel='Parceiro',
        email=data['email'],
        senha=password,
        validado=False
    )
    
    parceiro.nome = data['nome']
    parceiro.sobrenome = data['sobrenome']
    

    try:
        db.session.add(parceiro)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session().rollback()
        return jsonify({'Mensagem': 'O email informado já está cadastrado!'})

    
    # return send_email_confirm(parceiro.email)

    return jsonify({'Mensagem': 'Adicionado com sucesso!'})

@cp.route('/parceiro', methods=['PUT'])
@token_required
def edit_parceiro(current_user):
    parceiro = Parceiros.query.filter_by(id_geral=current_user.id_geral).first()

    if not parceiro:
        return jsonify({'Mensagem': 'Não encontrado!'})

    else:
        data = request.get_json()

        if data['cpf']:
            parceiros = Parceiros.query.all()
            for p in parceiros:
                if p.cpf == data['cpf'] and p.id_geral != parceiro.id_geral:
                    return jsonify({'mensagem': 'O CPF informado já está cadastrado'})
                else:
                    parceiro.cpf = data['cpf']

        if data['RA'] and data['matricula']:
            return jsonify({'Mensagem': 'Não é possível o mesmo usuário ter RA e matricula!'})

        if data['RA']:
            if not data['unidade']:
                return jsonify({'Mensagem': 'Não é possível cadastrar um aluno sem uma unidade de estudo!'})
            alunos = Alunos.query.filter_by().all()
            eAluno = False
            for aluno in alunos:
                if aluno.id_parceiros == current_user.id_geral:
                    eAluno = True

            if not eAluno:
                aluno_novo = Alunos(data['RA'], data['unidade'], current_user.id_geral)
                db.session.add(aluno_novo)
                db.session.commit()
            else:
                aluno = Alunos.query.filter_by(id_parceiros=current_user.id_geral).first()
                aluno.ra = data['RA']
                aluno.id_unidades = data['unidade']
                db.session.commit()

            parceiro.nivel = 'Aluno'

        if data['matricula']:
            parceiro.matricula = data['matricula']

        if data['nome']:
            parceiro.nome = data['nome']

        if data['sobrenome']:
            parceiro.sobrenome = data['sobrenome']

        if data['email']:
            parceiro.email = data['email']

        if data['senha']:
            if not parceiro.senha == 'Google account':
                senha = generate_password_hash(data['senha'])
                parceiro.senha = senha

        if data['rg']:
            parceiro.rg = data['rg']

        if data['foto_perfil']:
            parceiro.foto_perfil = data['foto_perfil']

        if data['dt_nascimento']:
            parceiro.dt_nascimento = data['dt_nascimento']

        if data['genero']:
            parceiro.genero = data['genero']

        if data['telefone']:
            parceiro.telefone = data['telefone']

        if data['local_trabalho']:
            parceiro.local_trabalho = data['local_trabalho']
        
        if data['cargo']:
            parceiro.cargo = data['cargo']

        if data['lattes']:
            parceiro.lattes = data['lattes']

        if data['facebook']:
            parceiro.facebook = data['facebook']

        if data['linkedin']:
            parceiro.linkedin = data['linkedin']

        if data['twitter']:
            parceiro.twitter = data['twitter']

        db.session.commit()

        return jsonify({'Mensagem': 'Alterado com sucesso!'})


@cp.route('/parceiro/<parceiro_id>', methods=['DELETE'])
@token_required
def del_parceiro(current_user, parceiro_id):
    parceiro = Parceiros.query.filter_by(id_geral=parceiro_id).first()

    if not parceiro:
        return jsonify({'Mensagem': 'Não encontrado!'})

    else:
        if parceiro.nivel == "Aluno":
            aluno = Alunos.query.filter_by(id_parceiros = parceiro_id).first()

            db.session.delete(aluno)
            db.session.commit()

        elif parceiro.nivel == "Diretor":
            diretor = Diretores.query.filter_by(id_parceiros = parceiro_id).first()
            
            db.session.delete(diretor)
            db.session.commit()

        elif parceiro.nivel == 'Agente':
            agente = Agentes.query.filter_by(id_parceiros = parceiro_id).first()

            db.session.delete(agente)
            db.session.commit()


        atividades = Atividades.query.filter_by(id_parceiro = parceiro_id).all()
        if atividades:
            for atividade in atividades:
                db.session.delete(atividade)
                db.session.commit()

        mensagens = Mensagens.query.filter_by(id_destinatarios = parceiro_id).all()
        if mensagens:
            for mensagem in mensagens:
                db.session.delete(mensagem)
                db.session.commit()

        inscricoes = Inscricoes.query.filter_by(id_parceiros = parceiro_id).all()
        if inscricoes:
            for inscricao in inscricoes:
                db.session.delete(inscricao)
                db.session.commit()

        avaliacoes = Avaliacoes.query.filter_by(id_avaliador = parceiro_id).all()
        if avaliacoes:
            for avaliacao in avaliacoes:
                db.session.delete(avaliacao)
                db.session.commit()
        
        db.session.delete(parceiro)
        db.session.commit()

        return jsonify({'Mensagem': 'Deletado com sucesso!'})


#********************************* Enviar Email  ***********************
def send_email_confirm(email):
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='dudsgrabbel@gmail.com', recipients=[email])

    link = url_for('.email_confirm', token = token, external = True)

    msg.body = 'Copie e Cole o link no seu navegador para confirmar seu email: \n\n {}'.format(link)    
    mail.send(msg)

    return jsonify({'Mensagem': 'Cadastrado com sucesso! Entre no seu E-mail para confirmar!'})


@cp.route('/emailconfirm/<token>')
def email_confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age = 90)

        parceiro = Parceiros.query.filter_by(email = email).first()

        if not parceiro:
            return jsonify({'Mensagem': 'Parceiro não encontrado'})
        
        parceiro.validado = True
        db.session.commit()

    except SignatureExpired:        
        return "link expirado!"

    return jsonify({'Mensagem': "E-mail verificado com sucesso!"})