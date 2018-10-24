from webapp import db, cp
from models.table_parceiros import Parceiros
from models.table_atividades import Atividades
from models.table_evento import Eventos
from models.table_material import Materiais
from models.table_inscricoes import Inscricoes
from models.table_agentes import Agentes
from models.table_mensagens import Mensagens
from models.table_diretores import Diretores
from models.table_eixos import Eixos
from models.table_inscricoes import Inscricoes
from models.table_unidades import Unidades
from models.table_avaliacoes import Avaliacoes
from flask import request, jsonify, redirect, url_for, session, render_template, make_response
import pdfkit
import random
from views.central_parceiros.login import token_required
from datetime import time, datetime, timedelta

def check_evento(id_evento):
    evento = Eventos.query.filter_by(id=id_evento).first()

    agora = datetime.now()
    agendamento = datetime(
        year = evento._data.year, 
        month = evento._data.month, 
        day = evento._data.day, 
        hour = evento.hora.hour, 
        minute = evento.hora.minute
    )

    agora = datetime.now()

    if agora > agendamento - timedelta(hours=1):
        return False
    else:
        return True

@cp.route('/evento', methods=['GET'])
@token_required
def get_eventos(current_user):
    eventos_geral = Eventos.query.all()
    eventos = [evento for evento in eventos_geral if evento.situacao == "Realizado" or evento.situacao == "Aprovado"]

    if not eventos:
        return jsonify({'Mensagem': 'Nenhum evento disponível!'})
    
    _eventos = []
    for evento in eventos:
        atividade = Atividades.query.filter_by(id=evento.id_atividades).first()
        parceiro = Parceiros.query.filter_by(id_geral=atividade.id_parceiro).first()
        unidade = Unidades.query.filter_by(id=evento.id_unidades).first()

        ev = {}
        ev['nome'] = atividade.titulo
        ev['autor'] = parceiro.nome
        ev['data'] = evento._data.strftime('%d/%m/%Y')
        ev['hora'] = str(evento.hora)
        ev['local'] = unidade.nome
        ev['banner'] = atividade.banner
        ev['id'] = evento.id
        ev['acesso'] = check_evento(evento.id)

        if 'token' in session:
            permissoes = ['Mestre', 'Administrador', 'Diretor']
            if evento.situacao == "Realizado" and current_user.nivel in permissoes:
                if current_user.nivel == 'Diretor':
                    unidade = Unidades.query.filter_by(id=evento.id_unidades).first()
                    diretor = Diretores.query.filter_by(id_unidades=unidade.id).first()
                    if current_user.id_geral != diretor.id_parceiros:
                        return jsonify({'Mensagem': 'Você não é o diretor da unidade deste evento'})

                avaliacoes = Avaliacoes.query.filter_by(id_evento=evento.id).all()

                if not avaliacoes:
                    ev['nota'] = '0 (0 avaliações)'
                else:
                    soma, count = 0, 0
                    for avaliacao in avaliacoes:
                        soma += avaliacao.nota
                        count += 1
                    nota = soma / count
                    ev['nota'] = '{} ({} avaliações)'.format(nota, len(avaliacoes))

        _eventos.append(ev)

    return jsonify(_eventos)

@cp.route('/evento/<int:id>', methods=['GET'])
@token_required
def get_one_evento(current_user, id):
    evento = Eventos.query.filter_by(id=id).first()

    if not evento or evento.situacao == False:
        return jsonify({'Mensagem': 'O evento requisitado não existe'})
        

    atividade = Atividades.query.filter_by(id=evento.id_atividades).first()
    parceiro = Parceiros.query.filter_by(id_geral=atividade.id_parceiro).first()
    unidade = Unidades.query.filter_by(id=evento.id_unidades).first()

    _evento = {}

    _evento['titulo'] = atividade.titulo
    _evento['descricao'] = atividade.descricao
    _evento['situacao'] = evento.situacao
    _evento['tipo'] = atividade.tipo
    _evento['duracao'] = atividade.duracao
    _evento['banner'] = atividade.banner
    _evento['acesso'] = check_evento(evento.id)
    _evento['data'] = evento._data.strftime('%d/%m/%Y')
    _evento['hora'] = str(evento.hora)
    _evento['local'] = unidade.nome
    _evento['endereco'] = unidade.endereco
    _evento['bairro'] = unidade.bairro
    _evento['cidade'] = unidade.cidade
    _evento['autor'] = parceiro.nome
    _evento['cargo_autor'] = parceiro.cargo
    _evento['trabalho_autor'] = parceiro.local_trabalho
    _evento['email_autor'] = parceiro.email

    permissoes = ['Mestre', 'Administrador', 'Diretor']
    if evento.situacao == "Realizado" and current_user.nivel in permissoes:
        if current_user.nivel == 'Diretor':
            unidade = Unidades.query.filter_by(id=evento.id_unidades).first()
            diretor = Diretores.query.filter_by(id_unidades=unidade.id).first()
            if current_user.id_geral != diretor.id_parceiros:
                return jsonify({'Mensagem': 'Você não é o diretor da unidade deste evento'})

        avaliacoes = Avaliacoes.query.filter_by(id_evento=evento.id).all()

        _comentarios = []
        for avaliacao in avaliacoes:
            comentarios = {}
            if avaliacao.identificar == True:
                parceiro = Parceiros.query.filter_by(id_geral=avaliacao.id_parceiro).first()
                comentarios['nome'] = parceiro.nome
            else:
                comentarios['nome'] = 'Anônimo'
            comentarios['comentario'] = avaliacao.comentario
            _comentarios.append(comentarios)
        _evento['comentarios'] = _comentarios

        if not avaliacoes:
            _evento['nota'] = '0 (0 avaliações)'
        else:
            soma, count = 0, 0
            for avaliacao in avaliacoes:
                soma += avaliacao.nota
                count += 1
            nota = soma / count
            _evento['nota'] = '{} ({} avaliações)'.format(nota, len(avaliacoes))

    return jsonify(_evento)

@cp.route('/evento', methods=['POST'])
@token_required
def post_evento(current_user):
    data = request.get_json()
    agentes = Agentes.query.all()

    id_agente = random.randint(1, len(agentes))

    # objeto da atividade
    atividade = Atividades(
        titulo = data['titulo'], 
        descricao = data['descricao'], 
        tipo = data['tipo'], 
        duracao = data['duracao'], 
        banner = data['banner'],
        id_agente = id_agente, 
        id_parceiro = current_user.id_geral
    )
    db.session.add(atividade)

  # objetos dos eventos
    eventos = data['eventos']

    
    obj_eventos = []
    for e in eventos:
        d = Diretores.query.filter_by(id_unidades = e[0]).first()
        evento = Eventos(
            id_atividades = atividade.id, 
            id_unidades = e[0], 
            _data = e[1], 
            hora = e[2],
            situacao = 'Aguardando análise da atividade'
        )
        obj_eventos.append(evento)

    # objetos dos materiais
    materiais = data['materiais']

    obj_materiais = []
    for m in materiais:
        material = Materiais(
            id_atividades = atividade.id,
            materia = m[0]
        )
        obj_materiais.append(material)

    # inserções no banco
    
    db.session.commit()

    for material in obj_materiais:
        db.session.add(material)
        db.session.commit()

    for evento in obj_eventos:
        db.session.add(evento)
        db.session.commit()

    agente = Agentes.query.filter_by(id=id_agente).first()
    parceiro = Parceiros.query.filter_by(id_geral=agente.id_parceiros).first()

    return redirect(url_for('.post_message', id_remetente = current_user.id_geral, id_destinatario = parceiro.id_geral, msg = 'Há uma nova atividade para avaliação: {}'.format(data['titulo'])), code=307)
    
#================= PUT ==========================
@cp.route('/evento/<evento_id>', methods=['PUT'])
@token_required
def edit_evento(current_user, evento_id):

    data = request.get_json()

    atividade = Atividades.query.filter_by(id = evento_id).first()

    if not atividade:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

    if current_user.id_geral != atividade.id_parceiro:
        return jsonify({'Mensagem': 'Você não é o criador deste evento'})

    eventos = data['eventos']

    post_evento = [e for e in eventos if not e[0]]
    put_evento = [e for e in eventos if e[0]]
    

    for e in post_evento:
        d = Diretores.query.filter_by(id_unidades = e[1]).first()
        
        evento = Eventos(
            id_atividades = evento_id, 
            id_unidades = e[1], 
            _data = e[2], 
            hora = e[3],
            id_diretor = d.id,
            situacao = False
        )

        db.session.add(evento)  
        db.session.commit()

    for e in put_evento:
        _evento = Eventos.query.filter_by(id = e[0]).first()
        
        _evento.unidade = e[1]
        _evento._data = e[2]
        _evento.hora = e[3]

        db.session.commit()

    materiais = data['materiais']

    post_material = [m for m in materiais if not m[0]]
    put_material = [m for m in materiais if m[0]]
    

    for m in post_material:
        material = Materiais(
            id_atividades = evento_id, 
            materia = m[1]
        )

        db.session.add(material)  
        db.session.commit()

    for m in put_material:
        _material = Materiais.query.filter_by(id = m[0]).first()
        
        _material.materia = m[1]

        db.session.commit()

    exclui_eventos = data['exclui_eventos']
    if exclui_eventos:
        for e in exclui_eventos:
            evento = Eventos.query.filter_by(id = e[0]).first()
            db.session.delete(evento)
            db.session.commit()

    
    exclui_materiais = data['exclui_materiais']
    if exclui_materiais:
        for m in exclui_materiais:
            material = Materiais.query.filter_by(id = m[0]).first()
            db.session.delete(material)
            db.session.commit()

    return jsonify({'Mensagem': "Atualizado com sucesso"})


@cp.route('/evento/<evento_id>', methods=['DELETE'])
@token_required
def del_evento(current_user, evento_id):

    atividade = Atividades.query.filter_by(id = evento_id).first()
    
    if not atividade:
        return jsonify({'Message': 'Evento não encontrado!'})

    if current_user.id_geral != atividade.id_parceiro:
        return jsonify({'Mensagem': 'Você não é o criador deste evento'})
        
    _materiais  = Materiais.query.filter_by(id_atividades = atividade.id).all()    
    _eventos = Eventos.query.filter_by(id_atividades = atividade.id).all()
    
    for m in _materiais:        
        db.session.delete(m)
        db.session.commit()
    
    for e in _eventos:
        inscricoes = Inscricoes.query.filter_by(id_eventos=e.id).all()

        for inscrito in inscricoes:
            db.session.delete(inscrito)
            db.session.commit()

        db.session.delete(e)
        db.session.commit()

    db.session.delete(atividade)
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso!'})


#****************** Inscrições no Evento *******************
@cp.route('/evento/<id_evento>/<acao>', methods=['GET'])
@token_required
def get_inscritos(current_user, id_evento, acao):
    _inscritos = Inscricoes.query.filter_by(id_eventos = id_evento).all()

    inscritos = []

    for inscrito in _inscritos:
        parceiro = Parceiros.query.filter_by(id_geral = inscrito.id_parceiros).first()

        info = {}
        info['id_parceiro'] = parceiro.id_geral
        info['nome'] = parceiro.nome
        info['email'] = parceiro.email
        info['presenca'] = inscrito.presenca

        inscritos.append(info)

    if acao == 'inscritos':  
        permissoes = ['Diretor', 'Administrador', 'Mestre']
        if not current_user.nivel in permissoes:
            return jsonify({'Mensagem': 'Você não tem Permissão'})
        return jsonify(inscritos)

    if acao == 'lista':
        permissoes = ['Diretor', 'Administrador', 'Mestre']
        if not current_user.nivel in permissoes:
            return jsonify({'Mensagem': 'Você não tem Permissão'})

        evento = Eventos.query.filter_by(id = id_evento).first()
        atividade = Atividades.query.filter_by(id = evento.id_atividades).first()

        #pasta temaplates com o arquivo 'pdf_inscritos.html', só para testes!
        rendered = render_template('pdf_inscritos.html', inscritos = inscritos, evento = atividade)
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-ype'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename = lista.pdf'

        return response

    if acao == 'certificado':
        permissoes = ['Diretor', 'Administrador', 'Mestre', 'Parceiro']
        if not current_user.nivel in permissoes:
            return jsonify({'Mensagem': 'Você não tem Permissão'})

        palestrante = Atividades.query.filter_by(id_parceiro = current_user.id_geral).first()

        if palestrante:
            info = get_one_evento(id_evento)
            rendered = render_template('certificado_palestrante.html', info = info.json, cpf = current_user.cpf)
            pdf = pdfkit.from_string(rendered, False)

            response = make_response(pdf)
            response.headers['Content-ype'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename = certificado.pdf'

            return response

        avaliacao = Avaliacoes.query.filter_by(id_evento = id_evento, id_parceiro = current_user.id_geral).first()
        
        if avaliacao == None:
            return jsonify({'Mensagem': 'Você não avaliou este evento!'})

        evento = Eventos.query.filter_by(id = id_evento).first()
        atividade = Atividades.query.filter_by(id = evento.id_atividades).first()
        unidade = Unidades.query.filter_by(id=evento.id_unidades).first()

        # nome da pessoa, tipo do evento, nome do evento, local do evento, data do evento
        
        for inscrito in inscritos:
            if current_user.id_geral == inscrito['id_parceiro']:
                info_certificado = {}

                info_certificado['nome_usuario'] = current_user.nome
                info_certificado['rg_usuario'] = current_user.rg
                info_certificado['tipo_evento'] = atividade.tipo
                info_certificado['nome_evento'] = atividade.titulo
                info_certificado['local_evento'] = unidade.nome
                info_certificado['data_evento'] = evento._data

                rendered = render_template('certificado.html', infos = info_certificado)
                pdf = pdfkit.from_string(rendered, False)

                response = make_response(pdf)
                response.headers['Content-ype'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename = certificado.pdf'

        return response
        
    return jsonify({'Mensagem': 'URL inválida'})

@cp.route('/evento/<id_evento>/inscrito', methods = ['POST'])
@token_required
def post_inscrito(current_user, id_evento):

    evento = Eventos.query.filter_by(id = id_evento).first()

    if evento.acesso is True:

        if check_evento(evento.id) == False:
            return jsonify({'Mensagem': 'Não é mais possível se cadastrar nesse evento!'})

        if evento.capacidade == evento.inscrito:
            return jsonify({'Mensagem': 'Evento Lotado!'})

        else:
            _inscrito = Inscricoes.query.filter_by(id_parceiros = current_user.id_geral, id_eventos = evento.id).first()

            if not _inscrito:
                inscricao = Inscricoes(current_user.id_geral, evento.id)
                db.session.add(inscricao)
                db.session.commit()

                novo = Eventos.query.filter_by(id = evento.id).first()
                novo.inscrito += 1

                db.session.commit()

                return jsonify({'Mensagem': 'Cadastrado com sucesso!'})
            
            return jsonify({'Mensagem': "Você já está cadastrado nesse evento!"})
        
    else:
        return jsonify({'Mensagem': 'As inscrições para esse evento foram encerradas!'})

@cp.route('/evento/<id_evento>/inscrito', methods=['DELETE'])
@token_required
def del_inscrito(current_user, id_evento):
    parceiro = Inscricoes.query.filter_by(id_parceiros = current_user.id_geral, id_eventos = id_evento).first()
    
    db.session.delete(parceiro)
    db.session.commit()
    
    evento = Eventos.query.filter_by(id = parceiro.id_eventos).first()

    evento.inscrito -= 1
    db.session.commit()

    return jsonify({'Mensagem': 'Inscrição cancelado com sucesso!'})




@cp.route('/evento/<id_evento>/inscritos/presenca', methods=['PUT'])
@token_required
def post_presenca(current_user, id_evento):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()
    
    inscritos = get_inscritos(id_evento, 'inscritos')

    lista = data['lista']

    for inscrito in inscritos.json:
        for l in lista:
            i = Inscricoes.query.filter_by(id_eventos = id_evento, id_parceiros = l['id_parceiro']).first()
            i.presenca = l['presenca']
            if l['presenca'] == True:

                parceiro = Parceiros.query.filter_by(id_geral=i.id_parceiros).first()

                mensagem = Mensagens(
                    descricao = 'Você tem um novo evento para avaliar', 
                    visualizacao = False, 
                    id_remetentes = current_user.id_geral, 
                    id_destinatarios = parceiro.id_geral
                )

                db.session.add(mensagem)
                db.session.commit()
            
            db.session.commit() 

    evento = Eventos.query.filter_by(id=id_evento).first()
    evento.situacao = 'Realizado'
    db.session.commit()
    
    insc = get_inscritos(id_evento, 'inscritos')
    
    return insc

@cp.route('/evento/<int:id>/avaliar', methods=['GET', 'POST'])
@token_required
def avaliacao(current_user, id):
    if request.method == 'POST':
        data = request.get_json()

        evento = Eventos.query.filter_by(id=id).first()

        if evento.situacao == 'Realizado':
            inscricao = Inscricoes.query.filter_by(id_eventos=evento.id, id_parceiros=current_user.id_geral).first()

            if not inscricao:
                return jsonify({'Mensagem': 'Você não se inscreveu neste evento!'})

            elif inscricao.presenca == False:
                return jsonify({'Mensagem': 'Você não compareceu a este evento!'})

            else:
                try:
                    if float(data['nota']) < 1 or float(data['nota']) > 5:
                        nota = data['nota']
                    else:
                        return jsonify({'Mensagem': 'A nota enviada precisa ser entre 1 e 5'})

                    avaliacao = Avaliacoes(
                        id_evento = evento.id, 
                        id_parceiro = current_user.id_geral, 
                        nota = float(data['nota']), 
                        comentario = data['comentario'], 
                        identificar = data['identificar']
                    )

                    db.session.add(avaliacao)
                    db.session.commit()

                    return jsonify({'Mensagem': 'Evento avaliado com sucesso!'})

                except ValueError:
                    return jsonify({'Mensagem': 'A nota precisa ser um valor numérico!'})
    else:
        inscricao = Inscricoes.query.filter_by(id_eventos=evento.id, id_parceiros=current_user.id_geral, situacao='Realizado').first()