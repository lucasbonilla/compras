# compras

Rodar make help

Não é necessário rodar nenhuma migration, o próprio build do projeto faz isso

Acessar em http://localhost:8080

Tabela para persistência:

CREATE TABLE IF NOT EXISTS public.atendimentos
(
    id integer NOT NULL DEFAULT nextval('atendimentos_id_seq'::regclass),
    cpf character varying(11) COLLATE pg_catalog."default" NOT NULL,
    private boolean NOT NULL,
    incompleto boolean NOT NULL,
    dta_u_compra date,
    tkt_medio double precision,
    tkt_u_compra double precision,
    loja_frequente character varying(14) COLLATE pg_catalog."default",
    loja_u_compra character varying(14) COLLATE pg_catalog."default",
    CONSTRAINT atendimentos_pkey PRIMARY KEY (id)
)

Em que:
  id = pk da tabela
  cpf = cpf do atendimento sem pontuações
  private = boolean
  incompleto = boolean
  dta_u_compra = data da última compra
  tkt_medio = valor médio do ticket
  tkt_u_compra = valor do último ticket
  loja_frequente = cnpj da loja mais frequente sem pontuações
  loja_u_compra = cnpj da loja da última compra sem pontuações