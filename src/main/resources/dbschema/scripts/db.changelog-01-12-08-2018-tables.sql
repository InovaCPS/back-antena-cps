--liquibase formatted sql

--changeset nadalete:01
--comment: creation the LOG table structure
CREATE TABLE parceiro (
	id SERIAL PRIMARY KEY,
	aluno boolean,
	ra integer,
	nome varchar(100) NOT NULL,
	email varchar(100) NOT NULL,
	cpf varchar(50) NULL,
	senha varchar(1000) NULL,

	rg varchar(15) NULL,
    dt_nascimento date NULL,
    genero varchar(15) NULL,
    telefone varchar(20) NULL,
    local_trabalho varchar(100) NULL,
    local_estudo varchar(100) NULL,
    
    lattes varchar(500) NULL,
    facebook varchar(500) NULL,
    linkedin varchar(500) NULL,
    twitter varchar(500) NULL

) WITH (
	OIDS=FALSE
);

CREATE TABLE tema_interesse ( 
    id SERIAL PRIMARY KEY, 
    nome VARCHAR(50) NOT NULL
) WITH (
	OIDS=FALSE
);


CREATE TABLE parceiro_tema (
    id SERIAL PRIMARY KEY, 
    tema INTEGER, 
    parceiro INTEGER, 
    FOREIGN KEY (tema) REFERENCES tema_interesse(id), 
    FOREIGN KEY (parceiro) REFERENCES parceiro(id)
) WITH (
	OIDS=FALSE
);

--rollback DROP TABLE LOG_LOG;