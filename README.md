# Central de Parceiros CPS

Este projeto tem como premissa a criação de ambientes para integração dos parceiros do CPS

## Equipe

A equipe envolvida neste projeto faz parte do INOVA Paula Souza, do CPS. Conheça melhor a equipe clicando [aqui](Equipe.md)

## Começando

(_em construção_)

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
* Instalando o PyBuilder - Projeto versionado
    ```bash
    git clone https://github.com/cpsinova/inova-log.git
    cd inova-log
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install pybuilder
    pyb install_dependencies
    pyb
    Depois: Verifique se target/dist/inova-log* foi criado
    ```

### Instruções opcionais - Use se necessário: ###

* Criando uma nova estrutura de projeto usando o PyBuilder
    ```bash
    pip intall pybuilder
    pyb --start-project
    pyb install_dependencies publish
    Depois: verifique se target/dist/inova-log* foi criado
    
    ```
* Atualizando todos os pacotes instalados na "venv"
 	1. Access **venv**
 	2. Execute: 
    ```bash 
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U 
    ```
* Fazendo upload do projeto para o repositório do PyPi
    ```bash
    pip install twine
    pyb
    twine upload -r pypi <caminho e nome do pacote tar.gz criato na pasta TARGET>
    ```
* Criando a base de dados do projeto
    * Pre-requerimentos (software)
        * Maven
        * JDK 1.8+
        * PostgreSQL Server - [Docker Postgres](https://hub.docker.com/_/postgres/)
    * Execute o seguinte comando
        * Criar base de dados
         ```bash
         mvn clean resources:resources liquibase:update
         ```
         * Limpar todas as bases
         ```bash
          mvn clean resources:resources liquibase:dropAll
         ```   
* Rode o projeto
    * Executar:
    ```bash
    ./runserver.sh

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
    "ra": "123456789", 
    "nome": "aluno", 
    "email": "email@email.com", 
    "cpf": "11111111", 
    "senha": "1234"
}
```
```bash
PUT - Atualiza um parceiro
/cp/parceiro/<id>

{
    "ra": "22222222222", 
    "nome": "aluno1", 
    "email": "email@email.com", 
    "cpf": "11111111", 
    "senha": "1234", 
    "rg": "", 
    "dt_nascimento": "", 
    "genero": "", 
    "telefone": "12345678", 
    "local_trabalho": "", 
    "local_estudo": "", 
    "lattes": "", 
    "facebook": "", 
    "linkedin": "", 
    "twitter": ""
}
```
```bash
DELETE - Apaga um parceiro
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
		["2", "1", "2018-10-15", "14:00"], 
		["2", "1", "2018-10-16", "14:00"], 
		["2", "1", "2018-10-17", "14:00"]
	], 
	"materiais":[
		["2", "caminho do material 1"], 
		["2", "caminho do material 2"]
	]
}

* Campos de "eventos": [id da atividade, id da unidade, data, hora]
* Campos de "materiais": [atividade, caminho do material]
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
		["1", "1", "2019-10-15", "12:30"], 
		["2", "1", "2019-10-16", "15:30"], 
		["3", "1", "2019-10-16", "20:30"],
		["", "1", "2020-10-17", "19:30"]
	], 
	"materiais":[
		["1", "caminho do material 10"],
		["2", "caminho do material 15"],
		["", "caminho do material 40"]
	], 
	"exclui_eventos": [
		["ID do evento"]
	], 
	"exclui_materiais": [
		["ID do material"]
	]
}

* Campos de "eventos": [id do evento, id da atividade, data, hora]
* Campos de "materiais": [id do material, caminho do material]
* Se "material" e/ou "evento" não tiverem um id, significa que são registros novos e precisam ser cadastrados
```
