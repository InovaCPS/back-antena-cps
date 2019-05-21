from webapp import db, cp, application
from models.table_projetos import Projetos
from models.table_arquivos import Arquivos
from models.table_cursos import Cursos
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

    # PARCEIRO
    parceiro = Parceiros.query.filter_by(id_geral = dados.id_parceiro).first()
    if parceiro is not None:
        projeto['id_parceiro'] = parceiro.id_geral
        projeto['nome_parceiro'] = "{} {}".format(parceiro.nome, parceiro.sobrenome)

    # UNIDADES
    idUnidadesRelacionadas = Rel_projeto_unidade.query.filter_by(id_projeto = dados.id).all()
    unidades = []
    for relacao in idUnidadesRelacionadas:
        unidade = Unidades.query.filter_by(id = relacao.id_unidade).first()
        infosUnidade = {}
        infosUnidade['id'] = unidade.id
        infosUnidade['nome'] = unidade.nome
        infosUnidade['cidade'] = unidade.cidade

        unidades.append(infosUnidade)
    
    projeto['unidades'] = unidades

    # CURSOS
    idCursosRelacionados = Rel_projeto_curso.query.filter_by(id_projeto = dados.id).all()
    cursos = []
    for relacao in idCursosRelacionados:
        curso = Cursos.query.filter_by(id = relacao.id_curso).first()
        infosCurso = {}
        infosCurso['id'] = curso.id
        infosCurso['nome'] = curso.nome

        cursos.append(infosCurso)
    
    projeto['cursos'] = cursos

    # PALAVRAS-CHAVE
    listaPalavras = Palavras_chave.query.filter_by(id_projeto = dados.id).all()
    palavrasChave = []
    for item in listaPalavras:
        infosPalavra = {}
        infosPalavra['palavra'] = item.palavra

        palavrasChave.append(infosPalavra)
    
    projeto['palavras-chave'] = palavrasChave

    # COLABORADORES
    idColaboradoresRelacionados = Rel_projeto_colaborador.query.filter_by(id_projeto = dados.id).all()
    colaboradores = []
    for relacao in idColaboradoresRelacionados:
        colaborador = Parceiros.query.filter_by(id_geral = relacao.id_colaborador).first()
        infosColaborador = {}
        infosColaborador['id'] = id
        infosColaborador['nome'] = "{} {}".format(colaborador.nome, colaborador.sobrenome)
        infosColaborador['email'] = colaborador.email

        colaboradores.append(infosColaborador)

    projeto['colaboradores'] = colaboradores

    # ARQUIVOS
    idArquivosRelacionados = Rel_projeto_arquivo.query.filter_by(id_projeto = dados.id).all()
    arquivos = []
    for relacao in idArquivosRelacionados:
        arquivo = Arquivos.query.filter_by(id = relacao.id_arquivo).first()
        infosArquivo = {}
        infosArquivo['tipo'] = arquivo.tipo
        infosArquivo['titulo'] = arquivo.titulo
        infosArquivo['descricao'] = arquivo.descricao
        infosArquivo['codigo'] = arquivo.codigo

        arquivos.append(infosArquivo)

    projeto['arquivos'] = arquivos

    # PREMIADO
    projeto['premiado'] = dados.premiado
    links = []
    if dados.premiado == True:
        linksRelacionados = Links.query.filter_by(id_projeto = dados.id).all()
        for link in linksRelacionados:
            infosLink = {}
            infosLink['URL'] = link.url

            links.append(infosLink)

    projeto['links'] = links

    # CATEGORIAS
    idCategoriasRelacionadas = Rel_projeto_categoria.query.filter_by(id_projeto = dados.id).all()
    categorias = []
    for relacao in idCategoriasRelacionadas:
        dadosCategoria = Categorias_projetos.query.filter_by(id = relacao.id_categoria).first()
        infosCategoria = {}
        infosCategoria['id'] = dadosCategoria.id
        infosCategoria['nome'] = dadosCategoria.categoria

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


'''
palavrasChave = data['palavrasChave']
    for palavra in palavrasChave:
        palavra = palavra.strip(" ")
        novaPalavra = Palavras_chave(
            id_projeto = projeto.id, 
            palavra = palavra
        )

        db.session.add(novaPalavra)
        db.session.commit()
 

    colaboradores = data['colaboradores']
    for colaborador in colaboradores:
        colaborador = colaborador.strip(" ")        
        colaborador = Parceiros.query.filter_by(email = colaborador).first()
        if not colaborador:
            pass # TEM Q FAZER TRATAMENTO DE EXCESSÃO AQUI
        else:
            projetoColaborador = Rel_projeto_colaborador(
                id_projeto = projeto.id, 
                id_colaborador = colaborador.id_geral
            )

            db.session.add(projetoColaborador)
            db.session.commit()
    
    if projeto.premiado == True:
        links = data['links']
        for link in links:
            link = link.strip(" ")
            link = Links(
                id_projeto = projeto.id, 
                url = link
            )

            db.session.add(link)
            db.session.commit()

    categorias = data['categorias']
    for categoria in categorias:
        projetoCategoria = Rel_projeto_categoria(
            id_projeto = projeto.id, 
            id_categoria = categoria['id']
        )

        db.session.add(projetoCategoria)
        db.session.commit()

    dadosArquivos = data['arquivos']
    for dado in dadosArquivos:
        nomeArquivo = dado['nomeMidia']
        extensao = nomeArquivo.split(".")[1]
        novoNome = str(hash('{}{}{}'.format(current_user.id_geral, str(datetime.datetime.now()), nomeArquivo))) + "." + extensao
        arquivo = request.files[dado['nomeMidia']]
        arquivo.filename = novoNome
        dado['nomeMidia'] = novoNome 

        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))

        infoArquivo = Arquivos(
            midia = dado['nomeMidia'], 
            titulo = dado['titulo'], 
            descricao = dado['descricao'], 
            codigo = dado['codigo'], 
            id_parceiro = current_user.id_geral
        )

        db.session.add(infoArquivo)
        db.session.commit()

        projetoArquivo = Rel_projeto_arquivo(
            id_projeto = projeto.id, 
            id_arquivo = infoArquivo.id
        )

        db.session.add(projetoArquivo)
        db.session.commit()
'''