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
from views.central_parceiros.avaliacao import avaliar
from datetime import time, datetime, timedelta

meses = [
        'janeiro', 'fevereiro', 'março', 'abril', 
        'maio', 'junho', 'julho', 'agosto', 
        'setembro', 'outubro', 'novembro', 'dezembro'
    ]

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

@token_required
def list_eventos(current_user, eventos):
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


@cp.route('/eventos', methods=['GET'])
@token_required
def get_eventos(current_user):
    eventos_geral = Eventos.query.all()
    eventos = [evento for evento in eventos_geral if evento.situacao == "Realizado" or evento.situacao == "Aprovado"]

    if not eventos:
        return jsonify({'Mensagem': 'Nenhum evento disponível!'})
    
    return list_eventos(eventos)

@cp.route('/meuseventos', methods=['GET'])
@token_required
def get_eventos_parceiro(current_user):
    inscritos = Inscricoes.query.filter_by(id_parceiros=current_user.id_geral).all()

    if not inscritos:
        return jsonify({'Mensagem': 'Você não se cadastrou em nenhum evento!'})

    eventos = []
    for inscrito in inscritos:
        info_evento = Eventos.query.filter_by(id=inscrito.id_eventos).first()

        eventos.append(info_evento)

    return list_eventos(eventos)

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

    _evento['id'] = evento.id
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
    _evento['id_local'] = evento.id_unidades
    _evento['endereco'] = unidade.endereco
    _evento['bairro'] = unidade.bairro
    _evento['cidade'] = unidade.cidade
    _evento['autor'] = parceiro.nome
    _evento['id_autor'] = parceiro.id_geral
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
                parceiro = Parceiros.query.filter_by(id_geral=avaliacao.id_avaliador).first()
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
        d = Diretores.query.filter_by(id_unidades = e['unidade']).first()
        evento = Eventos(
            id_atividades = atividade.id, 
            id_unidades = e['unidade'], 
            _data = e['data'], 
            hora = e['hora'],
            situacao = 'Aguardando análise da atividade'
        )
        obj_eventos.append(evento)

    # objetos dos materiais
    materiais = data['materiais']

    obj_materiais = []
    for m in materiais:
        material = Materiais(
            id_atividades = atividade.id,
            materia = m['material']
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

    post_evento = [e for e in eventos if not e['id']]
    put_evento = [e for e in eventos if e['id']]
    

    for e in post_evento:
        
        evento = Eventos(
            id_atividades = evento_id, 
            id_unidades = e['unidade'], 
            _data = e['data'], 
            hora = e['hora'],
            situacao = False
        )

        db.session.add(evento)  
        db.session.commit()

    for e in put_evento:
        _evento = Eventos.query.filter_by(id = e['id']).first()
        
        _evento.unidade = e[1]
        _evento._data = e[2]
        _evento.hora = e[3]

        db.session.commit()

    materiais = data['materiais']

    post_material = [m for m in materiais if not m['id']]
    put_material = [m for m in materiais if m['id']]
    

    for m in post_material:
        material = Materiais(
            id_atividades = evento_id, 
            materia = m['material']
        )

        db.session.add(material)  
        db.session.commit()

    for m in put_material:
        _material = Materiais.query.filter_by(id = m['id']).first()
        
        _material.materia = m['material']

        db.session.commit()

    exclui_eventos = data['exclui_eventos']
    if exclui_eventos:
        for e in exclui_eventos:
            evento = Eventos.query.filter_by(id = e['id']).first()
            db.session.delete(evento)
            db.session.commit()

    
    exclui_materiais = data['exclui_materiais']
    if exclui_materiais:
        for m in exclui_materiais:
            material = Materiais.query.filter_by(id = m['id']).first()
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
        response.headers['Content-type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename = lista.pdf'

        return response

    if acao == 'certificado':
        permissoes = ['Diretor', 'Administrador', 'Mestre', 'Parceiro', 'Agente', 'Aluno']
        if not current_user.nivel in permissoes:
            return jsonify({'Mensagem': 'Você não tem Permissão'})
        
        # Informações do evento atual em JSON
        info = get_one_evento(id_evento)
        info = info.json

        # Informações que serão enviadas ao renderizar o certificado
        info_certificado = {}

        info_certificado['nome_usuario'] = current_user.nome
        info_certificado['rg_usuario'] = current_user.rg

        # Informações do evento atual para pegar o mês
        evento_ = Eventos.query.filter_by(id=id_evento).first()

        # String informando a data para ser enviada ao certificado
        data = evento_._data.month - 1
        info_certificado['data_evento'] = "{}, {} de {} de {}".format(info['cidade'], evento_._data.day, meses[data], evento_._data.year)

        # Se o usuário atual for o palestrante do evento...
        palestrante = Atividades.query.filter_by(id_parceiro = current_user.id_geral).first()

        if palestrante:
            rendered = render_template('certificado_palestrante.html', info = info, cpf = current_user.cpf, data = info_certificado['data_evento'])
        else:
            # Percorre toda a lista de inscritos do atual evento para verificar se o usuário está inscrito
            inscricao = []
            for inscrito in inscritos:
                if inscrito['id_parceiro'] == current_user.id_geral:
                    inscricao.append(inscrito)
            
            if not inscricao:
                return jsonify({'Mensagem': 'Você não se inscreveu neste evento!'})

            for inscrito in inscritos:
                avaliacao = Avaliacoes.query.filter_by(id_evento = id_evento, id_avaliador = current_user.id_geral).first()
                if avaliacao != None:

                    rendered = render_template('certificado.html', infos = info_certificado, evento = info)
                else:
                    return jsonify({'Mensagem': 'Você ainda não avaliou este evento!'})

        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename = certificado.pdf'

        return response
        
    return jsonify({'Mensagem': 'URL inválida'})

@cp.route('/evento/<id_evento>/inscrito', methods = ['POST'])
@token_required
def post_inscrito(current_user, id_evento):

    evento = Eventos.query.filter_by(id = id_evento).first()
    if not evento:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

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

@cp.route('/evento/<id_evento>/inscrito', methods=['DELETE'])
@token_required
def del_inscrito(current_user, id_evento):
    inscricao = Inscricoes.query.filter_by(id_parceiros = current_user.id_geral, id_eventos = id_evento).first()
    if not inscricao:
        return jsonify({'Mensagem': 'Inscrição não encontrada!'})

    db.session.delete(inscricao)
    db.session.commit()
    
    evento = Eventos.query.filter_by(id = inscricao.id_eventos).first()

    evento.inscrito -= 1
    db.session.commit()

    return jsonify({'Mensagem': 'Inscrição cancelada com sucesso!'})




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
            db.session.commit() 
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

    evento = Eventos.query.filter_by(id=id_evento).first()
    evento.situacao = 'Realizado'
    db.session.commit()
    
    insc = get_inscritos(id_evento, 'inscritos')
    
    return insc

@cp.route('/evento/<int:id>/avaliar', methods=['POST'])
@token_required
def avaliacao_evento(current_user, id):
    data = request.get_json()

    evento = Eventos.query.filter_by(id=id).first()
    
    if not evento:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

    if evento.situacao == 'Realizado':
        inscricao = Inscricoes.query.filter_by(id_eventos=evento.id, id_parceiros=current_user.id_geral).first()
        palestrante = Atividades.query.filter_by(id = evento.id_atividades).first()
        if not inscricao:
            return jsonify({'Mensagem': 'Você não se inscreveu neste evento!'})

        elif inscricao.presenca == False:
            return jsonify({'Mensagem': 'Você não compareceu a este evento!'})

        else:
            resposta = avaliar(data, "Evento",id, palestrante.id_parceiro, current_user.id_geral)         
            return resposta
    else:    
        return jsonify({'Mensagem': 'Evento ainda em processo!'})
    
@cp.route('/evento/avaliacao', methods=['GET'])
@token_required
def parceiro_avaliações(current_user):
        inscricoes = Inscricoes.query.filter_by(id_parceiros=current_user.id_geral).all()
        eventos_avaliar = []
        for inscricao in inscricoes:
            evento_ = Eventos.query.filter_by(id = inscricao.id_eventos).first()
            if evento_.situacao == "Realizado":
                info = get_one_evento (id = evento_.id)
                
                eventos_avaliar.append(info.json)
            
        if not eventos_avaliar:
            return jsonify({'Mensagem': 'Nenhum evento disponivel para avaliação'})
            
        return jsonify(eventos_avaliar)


@cp.route('/evento/<int:id>/palestrante/<int:id_palestrante>/avaliar', methods=['POST'])
@token_required
def avaliacao_palestrante(current_user, id, id_palestrante):
    permissoes = ['Diretor']
    if not current_user.nivel in permissoes:
        return jsonify({'Mensagem': 'Você não tem Permissão'})

    data = request.get_json()

    evento = Eventos.query.filter_by(id=id).first()

    if not evento:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

    if evento.situacao == 'Realizado':
        palestrante = Parceiros.query.filter_by(id_geral=id_palestrante).first()
        diretor = Diretores.query.filter_by(id_parceiros = current_user.id_geral).first()
      
        if not palestrante:
            return jsonify({'Mensagem': 'Palestrante não encontrado!'})
        
        elif diretor.id_unidades != evento.id_unidades:
            return jsonify({'Mensagem': 'Você não tem permissão para avaliar esse Palestrante!'})

        else:
            resposta = avaliar(data, "Palestrante", id, id_palestrante, current_user.id_geral)         
            return resposta
    else:    
        return jsonify({'Mensagem': 'Evento ainda em processo!'})

@cp.route('/evento/<int:id>/unidade/avaliar', methods=['POST'])
@token_required
def avaliacao_unidade(current_user, id):
    data = request.get_json()

    evento = Eventos.query.filter_by(id=id).first()
    
    if not evento:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

    if evento.situacao == 'Realizado':
        parceiro = Atividades.query.filter_by(id = evento.id_atividades).first()
        unidade = Unidades.query.filter_by(id = evento.id_unidades).first()

        if not unidade:
            return jsonify({'Mensagem': 'Unidade não encontrada!'})

        elif parceiro.id_parceiro != current_user.id_geral:
            return jsonify({'Mensagem': 'Você não tem permisssão para avaliar a undade!'})

        else:
            resposta = avaliar(data, "Unidade",id, evento.id_unidades, current_user.id_geral)         
            return resposta
    else:    
        return jsonify({'Mensagem': 'Evento ainda em processo!'})