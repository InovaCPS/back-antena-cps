from webapp import db, cp, application
from models.table_projetos import Projetos
from models.table_arquivos import Arquivos
from models.table_cursos import Cursos
from models.table_alunos import Alunos
from models.table_links import Links
from models.table_palavras_chave import Palavras_chave
from models.table_relacao_projeto_arquivo import Rel_projeto_arquivo
from models.table_relacao_projeto_parceiro import Rel_projeto_colaborador
from models.table_rel_curso_unidade import Rel_Curso_Unidade
from models.table_relacao_projeto_categoria import Rel_projeto_categoria
from models.table_relacao_projeto_detalhes import Rel_projeto_detalhe
from models.table_parceiros import Parceiros
from models.table_unidades import Unidades
from models.table_categorias_projeto import Categorias_projetos
from views.central_parceiros.login import token_required
from flask import request, jsonify
import os, datetime, json

@cp.route('/projetos', methods=['POST'])
@token_required
def post_projeto(current_user):
    data = request.get_json()

    projeto = Projetos(
        titulo = data['titulo'], 
        descricao = data['descricao'], 
        orientador = data['orientador'],
        status = data['status'],
        tipo = data['tipo'],
        tema = data['tema']
    )
    if data['textoProjeto']:
        projeto.textoProjeto = data['textoProjeto']
    if data['linkTexto']:
        projeto.linkTexto = data['linkTexto']     

    db.session.add(projeto)    

    coops = data['coops']
    for coop in coops:
        parceiro = Parceiros.query.filter_by(email = coop['email']).first()

        if not parceiro:
            return jsonify({"Mensagem": "Usuario {} não encontrado".format(coop['email'])})
        else:
            projetoCoop = Rel_projeto_colaborador(
                id_projeto = projeto.id, 
                id_colaborador = parceiro.id_geral,
                tipo = "Coop"
            )

            db.session.add(projetoCoop)     

    if data['detalhes']: 
        detalhes = data['detalhes']       

        postDetalhes = Rel_projeto_detalhe(
            id_projeto = projeto.id,
            categoria1 = detalhes['categoria1'],
            categoria2 = detalhes['categoria2'],
            premio1 = detalhes['premio1'],
            premio2 = detalhes['premio2'],
            recurso1 = detalhes['recurso1'],
            recurso2 = detalhes['recurso2'],
            credito1 = detalhes['credito1'],
            credito2 = detalhes['credito2'],
            direitos = detalhes['direitos']
        )
        db.session.add(postDetalhes)

    if data['colaboradores']:
        colaboradores = data['colaboradores']
        for colaborador in colaboradores:
            parceiro = Parceiros.query.filter_by(email = colaborador['email']).first()

            if not parceiro:
                return jsonify({"Mensagem": "Usuario {} não encontrado".format(colaborador['email'])})
            else:
                projetoColaborador = Rel_projeto_colaborador(
                    id_projeto = projeto.id, 
                    id_colaborador = parceiro.id_geral,
                    tipo = "Colaborador"
                )
                db.session.add(projetoColaborador)
                db.session.commit()

                
    if data['arquivos']:
        arquivos = data['arquivos']

        for arquivo in arquivos:
            postArquivo = Arquivos(
                tipo = arquivo['tipo'],
                titulo = arquivo['titulo'],
                descricao = arquivo['legenda'],
                codigo = arquivo['link'],
                id_parceiro = current_user.id_geral
            )

            db.session.add(postArquivo)
            db.session.commit()

            projetoArquivo = Rel_projeto_arquivo(
                id_projeto = projeto.id, 
                id_arquivo = postArquivo.id
            )

            db.session.commit()
            db.session.add(projetoArquivo)
    
    if data['detalhes']: 
        db.session.commit()

    db.session.commit()
    db.session.commit()
    return jsonify({'Mensagem': 'Cadastrado com sucesso!'})

@cp.route('/projetos', methods=['GET'])
@token_required
def get_projetos(current_user):
    dados = Projetos.query.all()

    projetos = []

    for dado in dados:
        projeto = {}
        projeto['id'] = dado.id
        projeto['titulo'] = dado.titulo
        projeto['descricao'] = dado.descricao

        projetos.append(projeto)

    return jsonify(projetos)

@cp.route('/projetos/<int:id>', methods=['GET'])
@token_required
def get_projeto(current_user, id):
    dados = Projetos.query.filter_by(id = id).first()

    if not dados:
        return jsonify({'Mensagem': 'Projeto não encontrado!'})
    
    projeto = {}
    projeto['titulo'] = dados.titulo
    projeto['descricao'] = dados.descricao
    projeto['orientador'] = dados.orientador
    projeto['status'] = dados.status
    projeto['tipo'] = dados.tipo
    projeto['tema'] = dados.tema
    projeto['textoProjeto'] = dados.textoProjeto
    projeto ['linkTexto'] = dados.linkTexto

    # COOPS
    coops = Rel_projeto_colaborador.query.filter_by(id_projeto = dados.id).all()
    colaboradores = []
    cooperadores = []
    for coop in coops:        
        colaborador = Parceiros.query.filter_by(id_geral = coop.id_colaborador).first()
        if coop.tipo == "Coop":
            aluno = Alunos.query.filter_by(id_parceiros=colaborador.id_geral).first()
            unidade = Unidades.query.filter_by(id=aluno.id_unidades).first()
            curso = Cursos.query.filter_by(id = aluno.id_curso).first()

            info = {}
            info['email'] = colaborador.email
            info['escola'] = unidade.nome
            info['escola_curso'] = curso.nome

            cooperadores.append(info)
        else:
            infosColaborador = {}
            infosColaborador['id'] = id
            infosColaborador['nome'] = "{} {}".format(colaborador.nome, colaborador.sobrenome)
            infosColaborador['email'] = colaborador.email

            colaboradores.append(infosColaborador)

    projeto['coops'] = cooperadores
    projeto['colaboradores'] = colaboradores  

    # ARQUIVOS
    data_arquivos = Rel_projeto_arquivo.query.filter_by(id_projeto = dados.id).all()
    arquivos = []
    if data_arquivos:
        for data_arquivo in data_arquivos:
            arquivo = Arquivos.query.filter_by(id = data_arquivo.id_arquivo).first()
            infosArquivo = {}
            infosArquivo['tipo'] = arquivo.tipo
            infosArquivo['titulo'] = arquivo.titulo
            infosArquivo['legenda'] = arquivo.descricao
            infosArquivo['link'] = arquivo.codigo

            arquivos.append(infosArquivo)

    projeto['arquivos'] = arquivos  

    #Detalhes

    data_detalhes = Rel_projeto_detalhe.query.filter_by(id_projeto = dados.id).first()
   
    detalhes = {}
    if data_detalhes:
        detalhes['categoria1'] = data_detalhes.categoria1
        detalhes['categoria2'] = data_detalhes.categoria2
        detalhes['premio1'] = data_detalhes.premio1
        detalhes['premio2'] = data_detalhes.premio2
        detalhes['recurso1'] = data_detalhes.recurso1
        detalhes['recurso2'] = data_detalhes.recurso2
        detalhes['credito1'] = data_detalhes.credito1
        detalhes['credito2'] = data_detalhes.credito2
        detalhes['direitos'] = data_detalhes.direitos

    projeto['detalhes'] = detalhes

    return jsonify(projeto)

# ====================================================================
@cp.route('/projetos/categorias', methods=['GET'])
@token_required
def get_categorias(current_user):
    dadosCategorias = Categorias_projetos.query.all()

    listaCategorias = []
    for dado in dadosCategorias:
        categoria = {}
        categoria['id'] = dado.id
        categoria['nome'] = dado.categoria

        listaCategorias.append(categoria)
    
    return jsonify(listaCategorias)
