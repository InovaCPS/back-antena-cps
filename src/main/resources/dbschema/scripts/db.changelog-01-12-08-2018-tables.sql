--liquibase formatted sql

--changeset nadalete:01
--comment: creation the LOG table structure



-- *** estão sem sua Classe criada no models



--------------- Usuários do Sistema -------------------

-- Tabela de Parceiros
CREATE TABLE parceiros(
    id_geral SERIAL PRIMARY KEY,

    nivel VARCHAR(100) NOT NULL,    -- identificação atravez do back-end qual é a tabela
    
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(500) NOT NULL,

    cpf VARCHAR(50) NULL,
    rg VARCHAR(15) NULL,

    dt_nascimento date NULL,
    genero VARCHAR(15) NULL,
    
    local_trabalho VARCHAR(100) NULL,
    cargo VARCHAR(100) NULL,
    
    telefone VARCHAR(20) NULL,
    lattes VARCHAR(500) NULL,
    facebook VARCHAR(500) NULL,
    linkedin VARCHAR(500) NULL,
    twitter VARCHAR(500) NULL

) WITH (
    OIDS=FALSE
);

-- Tabela de Alunos
CREATE TABLE alunos (
	id SERIAL PRIMARY KEY,
	ra INTEGER,
    local_estudo VARCHAR(100) NULL,
    id_parceiros INTEGER,
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)

) WITH (
	OIDS=FALSE
);


-- Tabela de Regiões
CREATE TABLE regioes(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
) WITH (
    OIDS=FALSE
);

-- Tabela de Unidades
CREATE TABLE unidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(500) NOT NULL,
    id_regioes INTEGER,
    FOREIGN KEY (id_regioes) REFERENCES regioes(id)
) WITH (
    OIDS=FALSE
);

--Tabela de Agentes de Inovação
CREATE TABLE agentes (
    id SERIAL PRIMARY KEY,
    matricula VARCHAR(10) NOT NULL,
    id_unidades INTEGER,
    id_regioes INTEGER,
    id_parceiros INTEGER,
    hora TIME NULL,
    FOREIGN KEY (id_unidades) REFERENCES unidades(id),
    FOREIGN KEY (id_regioes) REFERENCES regioes(id),
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)
) WITH (
    OIDS=FALSE
);

-- Tabela de Atividades
CREATE TABLE atividades(
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    duracao INTEGER,
    banner VARCHAR(500) NOT NULL,
    id_agente INTEGER,
    situacao BOOLEAN,
    FOREIGN KEY (id_agente) REFERENCES Agentes(ID) --?
) WITH (
    OIDS=FALSE
);

--Tabela de Diretores
CREATE TABLE diretores(
    id SERIAL PRIMARY KEY,
    id_unidades INTEGER,
    id_parceiros INTEGER,
    FOREIGN KEY (id_unidades) REFERENCES unidades(id),
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)
) WITH(
    OIDS=FALSE
);

-- Tabela de Eventos
CREATE TABLE eventos(
    id SERIAL PRIMARY KEY,
    id_atividades INTEGER,
    id_unidades INTEGER,
    _data DATE,
    hora TIME,
    id_diretor INTEGER,
    situacao BOOLEAN,
    FOREIGN KEY (id_atividades) REFERENCES atividades(id),
    FOREIGN KEY (id_unidades) REFERENCES unidades(id),
    FOREIGN kEY (id_diretor) REFERENCES diretores(id)
) WITH (
    OIDS=FALSE
);


--Tabela de Administradores
CREATE TABLE adm (
    id SERIAL PRIMARY KEY,
    id_parceiros INTEGER,
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)
) WITH(
    OIDS=FALSE
);


-- Tabela de Materiais
CREATE TABLE materiais(
    id SERIAL PRIMARY KEY,
    id_atividades INTEGER,
    materia VARCHAR(500) NOT NULL,
    FOREIGN KEY (id_atividades) REFERENCES atividades(id)
) WITH (
    OIDS=FALSE
);



-- Tabela de Mensagens
CREATE TABLE mensagens(
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(500), 
    visualizacao VARCHAR(50),
    id_remetentes INTEGER,
    id_destinatarios INTEGER,
    FOREIGN KEY (id_remetentes) REFERENCES parceiros(id_geral),
    FOREIGN KEY (id_destinatarios) REFERENCES parceiros(id_geral)
) WITH(
    OIDS=FALSE
);

----------------------------------------
------------- Indefinidos --------------

CREATE TABLE tema_interesse ( 
    id SERIAL PRIMARY KEY, 
    nome VARCHAR(50) NOT NULL
) WITH (
	OIDS=FALSE
);


CREATE TABLE parceiro_tema (
    id SERIAL PRIMARY KEY, 
    id_tema INTEGER, 
    id_alunos INTEGER, 
    FOREIGN KEY (id_tema) REFERENCES tema_interesse(id), 
    FOREIGN KEY (id_alunos) REFERENCES alunos(id)
) WITH (
	OIDS=FALSE
);

--rollback DROP TABLE LOG_LOG;

---------------------------------------