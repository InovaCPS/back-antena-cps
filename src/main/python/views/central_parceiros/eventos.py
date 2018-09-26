from webapp import db, cp
from models.table_parceiros import Parceiros
from models.table_atividades import Atividades
from models.table_evento import Eventos
from models.table_material import Materiais
from models.table_agentes import Agentes
from models.table_mensagens import Mensagens
from models.table_diretores import Diretores
from models.table_eixos import Eixos
from flask import request, jsonify, redirect, url_for
import random
from views.central_parceiros.login import token_required


@cp.route('/evento', methods=['GET'])
def get_eventos():
    _atividades = Atividades.query.all()

    eventos = []

    for a in _atividades:
        ativ = {}
        ativ['titulo'] = a.titulo
        ativ['descricao'] = a.descricao
        ativ['tipo'] = a.tipo
        ativ['duracao'] = a.duracao
        ativ['banner'] = a.banner
        ativ['id_agente'] = a.id_agente        

        if not a.id_eixo:
            ativ['id_eixo'] = 'evento ainda não encaixado em um eixo!'
        else:
            eixo = Eixos.query.filter_by(id = a.id_eixo).first()
            ativ['eixo'] = eixo.nome

        _eventos = Eventos.query.filter_by(id_atividades = a.id).all()

        if not _eventos:
            ativ['evento'] = 'Nenhum evento cadastrado!'

        else:        
            evento = []

            for e in _eventos:
                eve = {}
                eve['id'] = e.id
                eve['id_unidades'] = e.id_unidades
                eve['_data'] = str(e._data)
                eve['hora'] = str(e.hora)
                eve['id_diretor'] = e.id_diretor
                eve['situacao'] = e.situacao

                evento.append(eve)

            ativ['evento'] = evento
        

        _materiais  = Materiais.query.filter_by(id_atividades = a.id).all()

        if not _materiais:
            ativ['material'] = 'Nenhum material cadastrado!'
        else:            
            mat = []
            for m in _materiais:
                material = {}
                material['id'] = m.id
                material['material'] = m.materia
                mat.append(material)
            
            ativ['material'] = mat

        eventos.append(ativ)

    return jsonify(eventos)

@cp.route('/evento/<evento_id>', methods=['GET'])
def get_one_evento(evento_id):
    a = Atividades.query.filter_by(id = evento_id).first()
    if not a:
        return jsonify({'Mensagem': 'Evento não encontrado!'})

    ativ = {}
    ativ['titulo'] = a.titulo
    ativ['descricao'] = a.descricao
    ativ['tipo'] = a.tipo
    ativ['duracao'] = a.duracao
    ativ['banner'] = a.banner
    ativ['id_agente'] = a.id_agente
    
    if not a.id_eixo:
        ativ['eixo'] = 'evento ainda não encaixado em um eixo!'
    else:
        eixo = Eixos.query.filter_by(id = a.id_eixo).first()
        ativ['eixo'] = eixo.nome
    
    _eventos = Eventos.query.filter_by(id_atividades = a.id).all()

    if not _eventos:
        ativ['evento'] = 'Nenhum evento cadastrado!'
    else:   
        evento = []

        for e in _eventos:
            eve = {}
            eve['id'] = e.id
            eve['id_unidades'] = e.id_unidades
            eve['_data'] = str(e._data)
            eve['hora'] = str(e.hora)
            eve['situacao'] = e.situacao

            evento.append(eve)

        ativ['evento'] = evento
        

    _materiais  = Materiais.query.filter_by(id_atividades = a.id).all()

    if not _materiais:
        ativ['materias'] = 'Nenhum material cadastrado!'
    else:
        mat = []
        for m in _materiais:
            material = {}
            material['id'] = m.id
            material['material'] = m.materia
            mat.append(material)
            
        ativ['material'] = mat

    return jsonify(ativ)

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
            situacao = False
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

    #atividade.titulo = data['titulo'], 
    #atividade.descricao = data['descricao'], 
    #atividade.tipo = data['tipo'], 
    #atividade.duracao = data['duracao'], 
    #atividade.banner = data['banner']

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
        
    _materiais  = Materiais.query.filter_by(id_atividades = atividade.id).all()    
    _eventos = Eventos.query.filter_by(id_atividades = atividade.id).all()
    
    for m in _materiais:        
        db.session.delete(m)
        db.session.commit()
    
    for e in _eventos:        
        db.session.delete(e)
        db.session.commit()

    db.session.delete(atividade)
    db.session.commit()

    return jsonify({'Mensagem': 'Deletado com sucesso!'})