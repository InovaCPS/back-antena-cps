from webapp import db, cp, app
from models.table_projetos import Projeto
from models.table_arquivos import Arquivo
from models.table_cursos import Curso
from models.table_links import Link
from models.table_palavras_chave import Palavra_chave
from models.table_relacao_projeto_arquivo import Rel_projeto_arquivo
from models.table_relacao_projeto_curso import Rel_projeto_curso
from models.table_relacao_projeto_parceiro import Rel_projeto_colaborador
from models.table_relacao_projeto_unidade import Rel_projeto_unidade
from models.table_parceiros import Parceiros
from models.table_unidades import Unidades
from views.central_parceiros.login import token_required
from flask import request
import os, datetime

@cp.route('/projetos', methods=['POST'])
@token_required
def post_projeto(current_user):
    arquivos = dict(request.files)
    arquivos = arquivos['arquivo']
    data = request.get_json()

    projeto = Projeto(
        titulo = data['titulo'], 
        descricao = data['descricao'], 
        id_parceiro = current_user.id_geral, 
        premiado = data['premiado']
    )

    db.session.add(projeto)
    db.session.commit()

    unidades = data['unidades']
    for unidade in unidades:
        unidade = Unidades.query.filter_by(id = unidade).first()
        if not unidade:
            pass # TEM Q FAZER TRATAMENTO DE EXCESSÃO AQUI
        else:
            projetoUnidade = Rel_projeto_unidade(
                id_projeto = projeto.id, 
                id_unidade = unidade.id
            )
        
            db.session.add(projetoUnidade)
            dn.session.commit()

    cursos = data['cursos']
    for curso in cursos:
        curso = Curso.query.filter_by(id=curso)
        if not curso:
            pass # TEM Q FAZER TRATAMENTO DE EXCESSÃO AQUI
        else:
            projetoCurso = Rel_projeto_curso(
                id_projeto = projeto.id, 
                id_curso = curso.id
            )

            db.session.add(projetoCurso)
            db.session.commit()


    palavrasChave = data['palavras-chave']
    for palavra in palavrasChave:
        novaPalavra = Palavra_chave(
            id_projeto = projeto.id, 
            palavra = palavra
        )

        db.session.add(novaPalavra)
        db.session.commit()
 

    colaboradores = data['colaboradores']
    for colaborador in colaboradores:
        colaborador = Parceiros.query.filter_by(id_geral = colaborador).first()
        if not colaborador:
            pass # TEM Q FAZER TRATAMENTO DE EXCESSÃO AQUI
        else:
            projetoColaborador = Rel_projeto_colaborador(
                id_projeto = projeto.id, 
                id_colaborador = colaborador.id_geral
            )
    
    if projeto.premiado == True:
        links = data['links_premiacao']
        for link in links:
            link = Link(
                id_projeto = projeto.id, 
                url = link
            )

            db.session.add(link)
            db.session.commit()

    dadosArquivos = data['arquivos']
    for arquivo in arquivos:
        for dado in dadosArquivos:
            if dado['midia'] == arquivo.filename:
                novoNome = hash('{}{}{}'.format(projeto.id, current_user.id_geral, str(datetime.datetime.now())))
                arquivo.filename = novoNome
                dado['midia'] = novoNome

                arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))

                infoArquivo = Arquivo(
                    midia = data['midia'], 
                    titulo = data['titulo'], 
                    descricao = data['descricao'], 
                    codigo = data['codigo'], 
                    id_parceiro = current_user.id_geral
                )

                db.session.add(infoArquivo)
                db.session.commit()

    return jsonify({'Mensagem': 'Cadastrado com sucesso!'})

@cp.route('/projetos', methods=['GET'])
@token_required
def get_projetos(current_user):
    dados = Projeto.query.all()

    projetos = []

    for dado in dados:
        projeto = {}
        projeto['titulo'] = dado.titulo
        projeto['descricao'] = dado.descricao

        projetos.append(projeto)

    return jsonify(projetos)

@cp.route('/projetos/<int:id>', methods=['GET'])
@token_required
def get_projeto(current_user, id):
    dados = Projeto.query.filter_by(id = id).first()

    if not dados:
        return jsonify({'Mensagem': 'Projeto não encontrado!'})
    
    projeto = {}
    projeto['titulo'] = dados.titulo
    projeto['descricao'] = dados.descricao

    # PARCEIRO
    parceiro = Parceiros.query.filter_by(id_geral = dados.id_parceiro)
    projeto['id_parceiro'] = parceiro.id_geral
    projeto['nome_parceiro'] = "{} {}".format(parceiro.nome, parceiro.sobrenome)

    # UNIDADES
    idUnidadesRelacionadas = Rel_projeto_unidade.query.filter_by(id_projeto = dados.id).all()
    unidades = []
    for id in idUnidadesRelacionadas:
        unidade = Unidades.query.filter_by(id = id).first()
        infosUnidade = {}
        infosUnidade['id'] = id
        infosUnidade['nome'] = unidade.nome
        infosUnidade['cidade'] = unidade.cidade

        unidades.append(infosUnidade)
    
    projeto['unidades'] = unidades

    # CURSOS
    idCursosRelacionados = Rel_projeto_curso.query.filter_by(id_projeto = dados.id).all()
    cursos = []
    for id in idCursosRelacionados:
        curso = Curso.query.filter_by(id = id).first()
        infosCurso = {}
        infosCurso['id'] = curso.id
        infosCurso['nome'] = curso.nome

        cursos.append(infosCurso)
    
    projeto['cursos'] = cursos

    # PALAVRAS-CHAVE
    palavras = Palavra_chave.query.filter_by(id_projeto = dados.id).all()
    palavrasChave = []
    for palavra in palavras:
        infosPalavra['palavra'] = palavra

        palavrasChave.append(infosPalavra)
    
    projeto['palavras-chave'] = palavrasChave

    # COLABORADORES
    idColaboradoresRelacionados = Rel_projeto_colaborador(id_projeto = dados.id).all()
    colaboradores = []
    for id in idColaboradoresRelacionados:
        colaborador = Parceiros.query.filter_by(id_geral = id).first()
        infosColaborador = {}
        infosColaborador['id'] = id
        infosColaborador['nome'] = "{} {}".format(colaborador.nome, colaborador.sobrenome)
        infosColaborador['email'] = colaborador.email

        colaboradores.append(infosColaborador)

    projeto['colaboradores'] = colaboradores

    # ARQUIVOS
    idArquivosRelacionados = Rel_projeto_arquivo(id_projeto = dados.id).all()
    arquivos = []
    for id in idArquivosRelacionados:
        arquivo = Arquivo.query.filter_by(id = id)
        infosArquivo = {}
        infosColaborador['midia'] = arquivo.midia
        infosColaborador['titulo'] = arquivo.titulo
        infosColaborador['descricao'] = arquivo.descricao
        infosColaborador['codigo'] = arquivo.codigo

        arquivos.append(infosArquivo)

    projeto['arquivos'] = arquivos

    # PREMIADO
    projeto['premiado'] = dados.premiado
    links = []
    if dados.premiado == True:
        linksRelacionados = Link.query.filter_by(id_projeto = dados.id).all()
        for link in linksRelacionados:
            infosLink = {}
            infosLink['URL'] = link.url

            links.append(infosLink)

    projeto['links'] = links


    return jsonify(projeto)