# Antena CPS

Este projeto tem como premissa a criação da maior e melhor plataforma de conexão entre alunos e o ecossistema.

A fim de virar uma comunidade, decidimos deixar algumas features disponíveis para que alunos e/ou interessados em colaborar possam ajudar no desenvolvimento, adquirindo experiencia, podendo usar sua contribuição como portfólio!


## Como Você pode Colaborar

Se você está a fim de ajudar no desenvolvimento, sempre disponibilizaremos "*bugs*" na aba de **Issues do repositorio**, bem como *features* no kanban disponivel em **Projects**, no projeto *Open Source*.

O Front-End do projeto está sendo construido em Angular CLi e o Back-End em Python e Flask!
Saiba mais sobre o Front-end clicando [aqui](https://github.com/InovaCPS/front-antena-cps/blob/master/README.md)

## Equipe

A equipe envolvida neste projeto faz parte do INOVA Paula Souza, do CPS. Conheça melhor a equipe clicando [aqui](Equipe.md)

## Project Charter

![image](https://user-images.githubusercontent.com/43144590/47235173-9c02ce80-d3ae-11e8-8521-2caf85c0d797.png)


## Começando

(_em construção_)

### Tutoriais
* [Flask - Videoaula](https://bit.ly/2z8N69x)
* [PostgreSQL com Linux - Videoaula](https://www.youtube.com/watch?v=-LwI4HMR_Eg)


Instruções para montar o projeto:
*  Criando um novo ambiente virtual (venv) para rodar junto ao Python 3
    ```bash
    python3 -m venv venv
    ```
ou
    ```bash
    virtualenv -p python3 venv
    ```
* Acessando o ambiente virtual **venv**
    ```bash
    source venv/bin/activate
    ```
* Atualizando a ferramenta "pip"
    ```bash
    pip install --upgrade pip
    ```
* Saindo do ambiente virtual **venv**
    ```bash
    deactivate
    ```

### Instruções opcionais - Use se necessário: ###

* Atualizando todos os pacotes instalados na "venv"
 	1. Access **venv**
 	2. Execute: 
    ```bash 
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U 
    ```
* Criando a base de dados do projeto
    * Pre-requerimentos (software)
        * Maven
        * JDK 1.8+
        * PostgreSQL Server - [Docker Postgres](https://hub.docker.com/_/postgres/)
    * Execute o seguinte comando
        * Desenvolvimento
            * Criar base de dados
            ```bash
            mvn clean resources:resources liquibase:update
            ```
            * Limpar todas as bases
            ```bash
            mvn clean resources:resources liquibase:dropAll
            ```   
        * Testes
            * Criar base de dados
            ```bash
              mvn clean resources:resources liquibase:update -Dprop='_qa'
            ```
            * Limpar todas as bases
            ```bash
              mvn clean resources:resources liquibase:dropAll -Dprop='_qa'
            ```   
* Rode o projeto
    * Executar:
    ```bash
    ./runserver.sh

### Documentação ###
Utilizamos uma adaptação do Swagger, o [Flasgger](https://github.com/rochacbruno/flasgger), para uma documentação visual da nossa API que pode ser acessada através da rota /apidocs.

### Endpoints: ###
```bash
GET - Retorna todos os parceiros
/cp/parceiro
```
```bash
GET - Retorna um parceiro
/cp/parceiro/<id>
```
```bash
POST - Cadastra um parceiro
/cp/parceiro

{
    "nome": "João", 
    "sobrenome": "Silva", 
    "email": "email@email.com", 
    "senha": "1234"
}
```
```bash
PUT - Atualiza informações do parceiro logado
/cp/parceiro/

{
    "nome": "João", 
    "sobrenome": "Santos", 
    "email": "email@email.com", 
    "cpf": "11111111", 
    "senha": "1234", 
    "rg": "", 
    "foto_perfil": "", 
    "dt_nascimento": "", 
    "genero": "", 
    "RA": "", 
    "unidade": "",
    "matricula": "", 
    "telefone": "12345678", 
    "local_trabalho": "", 
    "cargo": "",
    "lattes": "", 
    "facebook": "", 
    "linkedin": "", 
    "twitter": ""
}
```
```bash
DELETE - Exclui um parceiro
/cp/parceiro/<id>
```
```bash
GET - Retorna todos os eventos
/cp/evento
```
```bash
GET - Retorna um evento
/cp/evento/<id>
```
```bash
POST - Cadastra um evento
/cp/evento

{
	"titulo": "como programar Orientado a Objeto", 
	"descricao": "será explicado como programar Orientado a Objeto", 
	"tipo": "curso", 
	"duracao": "60", 
	"banner": "o caminho do banner", 
	"eventos":[
		{"unidade": "1", "data": "2018-10-15", "hora": "14:00"}, 
		{"unidade": "1", "data": "2018-10-16", "hora": "14:00"}, 
		{"unidade": "1", "data": "2018-10-17", "hora": "14:00"}
	], 
	"materiais":[
		{"material": "caminho do material 1"}, 
		{"material": "caminho do material 2"}
	]
}
```
```bash
PUT - Atualiza um evento
/cp/evento/<id>

{
	"titulo": "como programar C++", 
	"descricao": "será explicado como programar em C++", 
	"tipo": "curso", 
	"duracao": "40", 
	"banner": "o caminho do banner", 
	"eventos":[
		{"id": "1", "unidade": "1", "data": "2019-10-15", "hora": "12:30"}, 
		{"id": "2", "unidade": "1", "data": "2019-10-16", "hora": "15:30"}, 
		{"id": "3", "unidade": "1", "data": "2019-10-16", "hora: ""20:30"},
		{"id": "", "unidade": "1", "data": "2020-10-17", "hora": "19:30"}
	], 
	"materiais":[
		{"id": "1", "material": "caminho do material 10"},
		{"id": "2", "material": "caminho do material 15"},
		{"id": "", "material": "caminho do material 40"}
	], 
	"exclui_eventos": [
		["ID do evento"]
	], 
	"exclui_materiais": [
		["ID do material"]
	]
}

* Se "material" e/ou "evento" não tiverem um id, significa que são registros novos e precisam ser cadastrados
```

```bash
GET - Retorna todos os inscritos do evento
/cp/evento/<id>/inscritos
```
```bash
POST - Parceiro se cadastra no evento
/cp/evento/<id>/inscrito
```
```bash
DELETE - Parceiro se cancela inscrição no evento
/cp/evento/<id>/inscrito
```

```bash
PUT - Subir lista de presença do evento pro banco
/cp/evento/<id_evento>/inscritos/presenca

{
	"lista":[
		{    
		    "id_parceiro": "id_parceiro", 
		    "presenca": true or false
		},
		{    
		    "id_parceiro": "id_parceiro", 
		    "presenca": true or false
		}
	]
}
```
```bash
GET - Retornar todos os eventos com avaliação pendente
cp/evento/<id_evento>/avaliar
```
```bash
POST - Enviar avaliação do parceiro sobre o evento
cp/evento/<id_evento>/avaliar

{
    "nota": 4.5, 
    "comentario": "Excelente", 
    "identificar": true
}
```

```bash
GET - Retorna todos os Eventos que o parceiro deve avaliar
cp/evento/avaliacao
```
```bash
POST - Enviar avaliação do diretor sobre o palestrante e o seu evento na unidade
cp/evento/<id_evento>/palestrante/<id_palestrante>/avaliar

{
    "nota": 4.5, 
    "comentario": "Excelente", 
    "identificar": true
}
```
```bash
POST - Enviar avaliação do palestrante sobre a unidade
cp/evento/<id_evento>/unidade/avaliar

{
    "nota": 4.5, 
    "comentario": "Excelente", 
    "identificar": true
}
```

```bash
GET - Retorna todos os agentes
/cp/agentes
```
```bash
GET - Retorna um agente
/cp/agentes/<id>
```
```bash
POST - Cadastra um agente
/cp/agentes

{
    "id_parceiro": 1, 
    "hora": "30:00", 
    "matricula": 123123123, 
    "id_unidade": 1
}
```
```bash
PUT - Atualiza um agente
/cp/agentes/<id>

{
    "matricula": 123123123, 
    "hora": "30:00", 
    "id_unidade": 1, 
    "nome": "aluno1", 
    "sobrenome": "fatec", 
    "email": "email@email.com", 
    "cpf": "11111111", 
    "senha": "1234", 
    "rg": "", 
    "foto_perfil": "",
    "dt_nascimento": "", 
    "genero": "", 
    "telefone": "12345678", 
    "local_trabalho": "", 
    "cargo": "",
    "lattes": "", 
    "facebook": "", 
    "linkedin": "", 
    "twitter": ""
}
```
```bash
DELETE - Exclui um agente
/cp/agentes/<id>
```
```bash
GET - Retorna as atividades que o agente precisa enquadrar
/agentes/atividades
```
```bash
GET - Retorna todas as informações da atividade
/agentes/atividades/<id>
```
```bash
PUT - Atualiza a atividade
/agentes/atividades/<id>

{
    "eixo": 1
}
```
```bash
GET - Retorna as regiões e suas escolas
/cp/locais
```
```bash
GET - Retorna todos os Diretores
/cp/diretores
```
```bash
GET - Retorna um diretor
/cp/diretores/<id>
```
```bash
POST - Cadastra um diretor
/cp/diretores

{
    "id_unidade": 1,
    "id_parceiro": 1
}
```
```bash
PUT - Atualiza um diretor
/cp/diretores/<id>

{    
    "nome": "Diretor1", 
    "email": "diretor@gmail.com", 
    "cpf": "11111111", 
    "senha": "1234", 
    "rg": "46564", 
    "foto_perfil": "", 
    "dt_nascimento": "17/01/1982", 
    "genero": "Masculino", 
    "telefone": "12345678", 
    "local_trabalho": "CPS", 
    "cargo": "Professor",
    "lattes": "", 
    "facebook": "diretor1", 
    "linkedin": "", 
    "twitter": "diretor1"
}
```
```bash
DELETE - Deleta um diretor
/cp/diretores/<id>
```
```bash
GET - Retorna os eventos que o diretor precisa avaliar
/cp/diretores/atividades
```
```bash
GET - Retorna as informações do evento
/cp/diretores/<id>
```
```bash
PUT - Altera a situação do evento
/cp/diretores/<id>

{    
    "resposta": true, 
    "capacidade": 30
}
```

```bash
GET - Retorna nome e RA de todos os alunos
/cp/aluno
```
```bash
GET - Retorna as informações de um aluno
/cp/aluno/<ra>
```
```bash
POST - Cadastra um Aluno
/cp/aluno

{
    "ra": "5649454", 
    "id_parceiro": "1"
}
```
```bash
PUT - Atualiza o RA do aluno
/cp/aluno/RA


{
    "ra": "5649455"
}
```
```bash
DELETE - Deleta um aluno
/cp/aluno/<ra>
```
```bash
POST - Cadastra um Projeto
/cp/projetos
{
    "titulo":"teste Detalhe",
    "orientador":"orientador do projeto",
    "descricao": "Descricao do projeto",
    "status":"Status do projeto",
    "tipo":"Tipo do projeto",
    "tema":"Tema do projeto",
    "capa":"",
    "coops":[
    	{"email": "edu@hotmail.com"},
    	{"email": "teste1@hotmail.com"}
    ],
    "textoProjeto":"Texto projeto",
    "linkTexto": "Link Texto projeto",
    "arquivos":[
    	{
    		"tipo": "teste detalhe2",
    		"titulo": "Titulo Midia projeto",
    		"legenda": "legenda midia projeto",
    		"link": "Link midia projeto"
    	},
    	{
    		"tipo": "teste detalhe2",
    		"titulo": "Titulo Arquivo projeto",
    		"legenda": "legenda Arquivo projeto",
    		"link": "Link Arquivo projeto"
    	}
    ],
    "detalhes":
    	{
    		"categoria1": "teste categoria1",
    		"categoria2": "teste categoria2",
    		"premio1": "teste premio1",
    		"premio2": "teste premio2",
    		"recurso1": "teste recurso1",
    		"recurso2": "teste recurso2",
    		"credito1": "teste credito1",
    		"credito2": "teste credito2",
    		"direitos": "teste direitos"
    	},
    "colaboradores":[
    	{"email": "edu-simao@outlook.com"}
    ]
}
```
```bash
GET - Retorna todos os projetos cadastrado
/cp/projetos
```
```bash
GET - Retorna todos os projetos cadastrado do Aluno
/cp/projetos/aluno
```
```bash
GET - Retorna todos os dados do projeto
/cp/projetos/<id_projeto>
```
```bash
PUT - Atualiza todos os dados do projeto
/cp/projetos
{
    "arquivos": [
        {
            "id_arquivo": "id_arquivo",
            "legenda": "legenda midia projeto",
            "link": "Link midia projeto",
            "tipo": "teste detalhe2",
            "titulo": "Titulo Midia projeto"
        },
        {
            "id_arquivo": "id_arquivo",
            "legenda": "legenda Arquivo projeto",
            "link": "Link Arquivo projeto",
            "tipo": "teste detalhe2",
            "titulo": "Titulo Arquivo projeto"
        },
        {
            "id_arquivo": "",
            "legenda": "legenda Codigo projeto",
            "link": "Link Arquivo projeto",
            "tipo": "codigo",
            "titulo": "Titulo Codigo projeto"
        }
    ],
    "capa": "",
    "colaboradores": [
        {
            "email": "edu-simao@outlook.com",
            "id": "id_colaboradores"
        },
        {
            "email": "teste1@hotmail.com",
            "id": ""
        }
    ],
    "coops": [
        {
            "email": "edu@hotmail.com",
            "id": "id_coop"
        },
        {
            "email": "edu@hotmail.com",
            "id": ""
        }
    ],
    "descricao": "teste Detalhe",
    "detalhes": {
        "categoria1": "teste categoria1",
        "categoria2": "teste categoria2",
        "credito1": "teste credito1",
        "credito2": "teste credito2",
        "direitos": "teste direitos",
        "id_detalhes": "11",
        "premio1": "teste premio1",
        "premio2": "teste premio2",
        "recurso1": "teste recurso1",
        "recurso2": "teste recurso2"
    },
    "id_projeto": "id_projeto",
    "linkTexto": "Link Texto projeto",
    "orientador": "orientador do projeto",
    "status": "Status do projeto",
    "tema": "Tema do projeto",
    "textoProjeto": "Texto projeto",
    "tipo": "Tipo do projeto",
    "titulo": "teste Detalhe"
}
```

### Instruções Login - Postman ###

```bash

URL -
    /login

* Aba Authorization:

    type -> Basic Auth

    username -> email cadastrado na tabela Parceiro
    password -> senha cadastrada na Tabela Parceiro

    clicar em send e copiar a token gerada

* Aba Headers:

    key -> token
    value -> Token gerada
```
