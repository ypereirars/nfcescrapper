CREATE TABLE public.usuarios (
	id bigserial NOT NULL PRIMARY KEY,
	primeiro_nome varchar(100) NOT NULL,
	ultimo_nome varchar(100) NOT NULL,
	nome_usuario varchar(100) NOT NULL,
	data_criacao timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.empresas (
	id bigserial NOT NULL PRIMARY KEY,
	cnpj varchar(20) NOT NULL,
	razao_social text NOT NULL,
	logradouro text NULL,
	numero text NULL,
	complemento text NULL,
	bairro text NULL,
	municipio text NULL,
	uf varchar(2) NULL,
	cep varchar(10) NULL,
	CONSTRAINT empresas_unique UNIQUE (cnpj),
	data_criacao timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.produtos (
	id bigserial PRIMARY key,
	codigo varchar NOT NULL,
	descricao text NOT NULL,
	data_criacao timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.notas_fiscais (
	id bigserial NOT NULL PRIMARY key,
	id_empresa bigserial REFERENCES empresas(id) ON DELETE SET NULL ON UPDATE CASCADE,
	id_usuario bigserial REFERENCES usuarios(id) ON DELETE SET NULL ON UPDATE CASCADE,
	chave_acesso varchar(50) NOT NULL,
	numero varchar NOT NULL, 
	serie varchar NOT NULL,
	protocolo_autorizacao varchar NOT NULL,
	data_autorizacao timestamp DEFAULT NULL,
	data_emissao timestamp DEFAULT NULL,
	tributacao_federal decimal NOT NULL DEFAULT 0.0,
	tributacao_estadual decimal NOT NULL DEFAULT 0.0,
	tributacao_municipal decimal NOT NULL DEFAULT 0.0,
	fonte varchar DEFAULT NULL,
	data_criacao timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE public.itens_nota (
	id bigserial NOT NULL PRIMARY KEY,
	id_produto bigserial REFERENCES produtos(id) ON DELETE SET NULL ON UPDATE CASCADE,
	id_nota_fiscal bigserial REFERENCES notas_fiscais(id) ON DELETE SET NULL ON UPDATE CASCADE,
	quantidade decimal NULL DEFAULT 0,
	preco_unitario decimal NOT NULL DEFAULT 0.0,
	unidade_medida varchar DEFAULT NULL,
	id_empresa bigserial REFERENCES empresas(id) ON DELETE SET NULL ON UPDATE CASCADE
);