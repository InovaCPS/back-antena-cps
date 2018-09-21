from webapp import app, db, cp
from models.table_parceiros import Parceiros
from models.table_atividades import Atividades
from models.table_evento import Eventos
from models.table_material import Materiais
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


@cp.route('/evento', methods=['GET'])
def get_eventos():
    _atividades = Atividades.query.all()

    eventos = []

    for a in _atividades:
        ativ = {}
        ativ['id'] = a.id
        ativ['titulo'] = a.titulo
        ativ['descricao'] = a.descricao
        ativ['tipo'] = a.tipo
        ativ['duracao'] = a.duracao
        ativ['banner'] = a.banner

        _eventos = Eventos.query.filter_by(id_atividades=a.id).all()
        evento = []

        for e in _eventos:
            eve = {}
            eve['id_atividades'] = e.id_atividades
            eve['id_unidades'] = e.id_unidades
            eve['_data'] = str(e._data)
            eve['hora'] = str(e.hora)

            evento.append(eve)

        ativ['evento'] = evento

        _materiais = Materiais.query.filter_by(id_atividades=a.id).all()
        mat = []
        for m in _materiais:
            material = {}
            material['id_atividades'] = m.id_atividades
            material['material'] = m.materia
            mat.append(material)

        ativ['material'] = mat

        eventos.append(ativ)

    return jsonify(eventos)


@cp.route('/evento/<evento_id>', methods=['GET'])
def get_one_evento(evento_id):
    a = Atividades.query.filter_by(id=evento_id).first()
    if not a:
        return jsonify({'Message': 'Evento não encontrado!'})

    ativ = {}
    ativ['titulo'] = a.titulo
    ativ['descricao'] = a.descricao
    ativ['tipo'] = a.tipo
    ativ['duracao'] = a.duracao
    ativ['banner'] = a.banner

    _eventos = Eventos.query.filter_by(id_atividades=a.id).all()
    evento = []

    for e in _eventos:
        eve = {}
        eve['id_atividades'] = e.id_atividades
        eve['id_unidades'] = e.id_unidades
        eve['_data'] = str(e._data)
        eve['hora'] = str(e.hora)

        evento.append(eve)

    ativ['evento'] = evento

    _materiais = Materiais.query.filter_by(id_atividades=a.id).all()
    mat = []
    for m in _materiais:
        material = {}
        material['id_atividades'] = m.id_atividades
        material['materia'] = m.materia
        mat.append(material)

    ativ['material'] = mat

    return jsonify(ativ)


@cp.route('/evento', methods=['POST'])
def post_evento():
    data = request.get_json()

    # objeto da atividade
    atividade = Atividades(
        titulo=data['titulo'],
        descricao=data['descricao'],
        tipo=data['tipo'],
        duracao=data['duracao'],
        banner=data['banner'])

    # objetos dos eventos
    eventos = data['eventos']

    obj_eventos = []
    for e in eventos:
        evento = Eventos(e[0], e[1], e[2], e[3])
        obj_eventos.append(evento)

    # objetos dos materiais
    materiais = data['materiais']

    obj_materiais = []
    for m in materiais:
        material = Materiais(m[0], m[1])
        obj_materiais.append(material)

    # inserções no banco
    db.session.add(atividade)
    db.session.commit()

    for material in obj_materiais:
        db.session.add(material)
        db.session.commit()

    for evento in obj_eventos:
        db.session.add(evento)
        db.session.commit()

    return jsonify({'message': 'Cadastrado com sucesso!'})


#================= PUT ==========================
@cp.route('/evento/<evento_id>', methods=['PUT'])
def edit_evento(evento_id):
    data = request.get_json()

    atividade = Atividades.query.filter_by(id=evento_id).first()
    if not atividade:
        return jsonify({'Message': 'Evento não encontrado!'})

    atividade.titulo = data['titulo'],
    atividade.descricao = data['descricao'],
    atividade.tipo = data['tipo'],
    atividade.duracao = data['duracao'],
    atividade.banner = data['banner']

    eventos = data['eventos']

    post_evento = [e for e in eventos if not e[0]]
    put_evento = [e for e in eventos if e[0]]

    for e in post_evento:
        evento = Eventos(
            atividade=evento_id, unidade=e[1], _data=e[2], hora=e[3])

        db.session.add(evento)
        db.session.commit()

    for e in put_evento:
        _evento = Eventos.query.filter_by(id=e[0]).first()

        _evento.unidade = e[1]
        _evento._data = e[2]
        _evento.hora = e[3]

        db.session.commit()

    materiais = data['materiais']

    post_material = [m for m in materiais if not m[0]]
    put_material = [m for m in materiais if m[0]]

    for m in post_material:
        material = Material(atividade=evento_id, materia=m[1])

        db.session.add(material)
        db.session.commit()

    for m in put_material:
        _material = Material.query.filter_by(id=m[0]).first()

        _material.materia = m[1]

        db.session.commit()

    exclui_eventos = data['exclui_eventos']

    for e in exclui_eventos:
        evento = Eventos.query.filter_by(id=e[0]).first()
        db.session.delete(evento)
        db.session.commit()

    exclui_materiais = data['exclui_materiais']

    for m in exclui_materiais:
        material = Material.query.filter_by(id=m[0]).first()
        db.session.delete(material)
        db.session.commit()

    return jsonify({'Message': "Atualizado com sucesso"})


@cp.route('/evento/<evento_id>', methods=['DELETE'])
def del_evento(evento_id):
    atividade = Atividades.query.filter_by(id=evento_id).first()

    if not atividade:
        return jsonify({'Message': 'Evento não encontrado!'})

    _materiais = Material.query.filter_by(atividade=atividade.id).all()

    _eventos = Eventos.query.filter_by(atividade=atividade.id).all()

    for m in _materiais:
        db.session.delete(m)
        db.session.commit()

    for e in _eventos:
        db.session.delete(e)
        db.session.commit()

    db.session.delete(atividade)
    db.session.commit()

    return jsonify({'message': 'Evento deletado com sucesso!'})