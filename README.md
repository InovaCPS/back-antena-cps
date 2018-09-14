# Central de Parceiros CPS

Este projeto tem como premissa a criação de ambientes para integração dos parceiros do CPS

## Equipe

A equipe envolvida neste projeto faz parte do INOVA Paula Souza, do CPS. Conheça melhor a equipe clicando [aqui](Equipe.md)

(_in construction_)

Instructions to build the project:
*  Creating a new virtual environment (venv) to run with Python 3
    ```bash
    python3 -m venv venv
    ```
or
    ```bash
    virtualenv -p python3 venv
    ```
* Accessing virtual environment **venv**
    ```bash
    source venv/bin/activate
    ```
Updating "pip" tool
    ```bash
    pip install --upgrade pip
    ```
* Exiting of virtual environment **venv**
    ```bash
    deactivate
    ```
* Installing PyBuilder - Versioned project
    ```bash
    git clone https://github.com/cpsinova/inova-log.git
    cd inova-log
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install pybuilder
    pyb install_dependencies
    pyb
    After: verifify if target/dist/inova-log* was created
    ```

### Optional instructions - Use if necessary: ###

* Creating a new project structure using PyBuilder
    ```bash
    pip intall pybuilder
    pyb --start-project
    pyb install_dependencies publish
    After: verifify if target/dist/inova-log* was created
    
    ```
* Updating all packages installed in "venv"
 	1. Access **venv**
 	2. Execute: 
    ```bash 
    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U 
    ```
* Uploading the project do PyPi respository
    ```bash
    pip install twine
    pyb
    twine upload -r pypi <path and name of the package tar.gz created into the TARGET folder>
    ```
* Creating the project database
    * Pre-requirements (software)
        * Maven
        * JDK 1.8+
        * PostgreSQL Server - [Docker Postgres](https://hub.docker.com/_/postgres/)
    * Execute the follow command
        * Create database
         ```bash
         mvn clean resources:resources liquibase:update
         ```
         * Clean all database
         ```bash
          mvn clean resources:resources liquibase:dropAll
         ```   
* Run the project
    * Execute:
    ```bash
    ./runserver.sh


Exemplo json POST

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

Na hora de dar um Post no Evento os campos da lista eventos são:
[atividade, unidade, _data, hora]

e os materias são:
[atividade, caminho do material]


Exemplo json PUT


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
	]
}

 Já na hora do PUT, os campos mudam!
 Nos eventos são:
[id do evento, id da atividade, _data, hora]

e os materias são:
[id do material, caminho do material]

caso o material e/ou evento não tenham id, eles foram adicionado no front e deve ser feito um post