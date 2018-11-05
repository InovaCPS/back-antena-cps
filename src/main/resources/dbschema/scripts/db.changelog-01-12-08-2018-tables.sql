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
    sobrenome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
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
    twitter VARCHAR(500) NULL, 
    validado BOOLEAN

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
    endereco VARCHAR(300) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    id_regioes INTEGER,
    FOREIGN KEY (id_regioes) REFERENCES regioes(id)
) WITH (
    OIDS=FALSE
);

-- Tabela de Alunos
CREATE TABLE alunos (
	id SERIAL PRIMARY KEY,
	ra INTEGER,
    id_unidades INTEGER,
    id_parceiros INTEGER,
    FOREIGN KEY (id_unidades) REFERENCES unidades(id),
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)

) WITH (
	OIDS=FALSE
);

--Tabela de Agentes de Inovação
CREATE TABLE agentes (
    id SERIAL PRIMARY KEY,
    matricula VARCHAR(10) NOT NULL,
    id_unidades INTEGER,
    id_parceiros INTEGER,
    hora VARCHAR(8) NULL,
    FOREIGN KEY (id_unidades) REFERENCES unidades(id),
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral)
) WITH (
    OIDS=FALSE
);

--Tabela de Eixos Tecnológicos
CREATE TABLE eixos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100)
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
    id_eixo INTEGER,
    id_parceiro INTEGER,
    FOREIGN KEY (id_agente) REFERENCES Agentes(ID),
    FOREIGN KEY (id_eixo) REFERENCES eixos(id),
    FOREIGN KEY (id_parceiro) REFERENCES parceiros(id_geral)
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
    situacao VARCHAR(40),
    capacidade INTEGER,
    inscrito INTEGER,
    acesso BOOLEAN, -- Disponibilidade para se inscrever no evento
    FOREIGN KEY (id_atividades) REFERENCES atividades(id),
    FOREIGN KEY (id_unidades) REFERENCES unidades(id)
) WITH (
    OIDS=FALSE
);

-- Tabela de Inscrições
CREATE TABLE inscricoes(
    id SERIAL PRIMARY KEY,
    id_parceiros INTEGER,
    id_eventos INTEGER,
    presenca BOOLEAN,
    FOREIGN KEY (id_parceiros) REFERENCES parceiros(id_geral),
    FOREIGN KEY (id_eventos) REFERENCES eventos(id)
) WITH (
    OIDS=FALSE
);

-- Tabela de Avaliações
CREATE TABLE avaliacoes(
    id SERIAL PRIMARY KEY, 
    id_evento INTEGER, 
    id_parceiro INTEGER, 
    nota FLOAT, 
    comentario VARCHAR(250), 
    identificar BOOLEAN, 
    FOREIGN KEY (id_evento) REFERENCES eventos(id), 
    FOREIGN KEY (id_parceiro) REFERENCES parceiros(id_geral)
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

-- Inserções de teste do banco de desenvolvimento
-- EXCLUIR QUANDO ENVIAR PARA PRODUÇÃO

--INSERT INTO parceiros (nivel, nome, email, senha) 
--VALUES ('Parceiro', 'João', 'joao@gmail.com', '321');

--INSERT INTO parceiros (nivel, nome, email, senha) 
--VALUES ('Agente', 'Maria', 'maria@gmail.com', '123');

--INSERT INTO parceiros (nivel, nome, email, senha) 
--VALUES ('Diretor', 'José', 'jose@gmail.com', '213');

INSERT INTO regioes (nome)
VALUES ('Baixada Santista');

INSERT INTO unidades (nome, endereco, bairro, cidade, id_regioes)
VALUES ('FATEC PG', 'Praça 19 de Janeiro, 144', 'Boqueirão', 'Praia Grande', 1);

--INSERT INTO agentes (matricula, id_unidades, id_parceiros, hora)
--VALUES (12345679, 1, 2, '30:00');

--INSERT INTO diretores (id_unidades, id_parceiros)
--VALUES (1, 3);

INSERT INTO eixos (nome)
VALUES ('Tecnologia');

INSERT INTO eixos (nome)
VALUES ('Outros');