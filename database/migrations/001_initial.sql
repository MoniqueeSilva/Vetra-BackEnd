CREATE TABLE estabelecimentos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(14) UNIQUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE usuarios (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE estabelecimento_usuarios (
    estabelecimento_id BIGINT NOT NULL REFERENCES estabelecimentos(id),
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    perfil VARCHAR(20) NOT NULL DEFAULT 'ADM',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (estabelecimento_id, usuario_id),
    CHECK (perfil IN ('ADM'))
);

CREATE TABLE categorias (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL REFERENCES estabelecimentos(id),
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (estabelecimento_id, nome),
    UNIQUE (id, estabelecimento_id)
);

CREATE TABLE produtos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL REFERENCES estabelecimentos(id),
    categoria_id BIGINT NOT NULL,
    codigo VARCHAR(50) NOT NULL,
    nome VARCHAR(150) NOT NULL,
    marca VARCHAR(100),
    unidades_por_caixa INTEGER NOT NULL DEFAULT 1,
    custo_unitario NUMERIC(12,2) NOT NULL DEFAULT 0,
    preco_unitario NUMERIC(12,2) NOT NULL,
    preco_caixa NUMERIC(12,2),
    estoque_minimo INTEGER NOT NULL DEFAULT 0,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (estabelecimento_id, codigo),
    UNIQUE (id, estabelecimento_id),

    FOREIGN KEY (categoria_id, estabelecimento_id)
        REFERENCES categorias(id, estabelecimento_id),

    CHECK (unidades_por_caixa > 0),
    CHECK (custo_unitario >= 0),
    CHECK (preco_unitario >= 0),
    CHECK (preco_caixa IS NULL OR preco_caixa >= 0),
    CHECK (estoque_minimo >= 0)
);

CREATE TABLE estoques (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL,
    produto_id BIGINT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (estabelecimento_id, produto_id),

    FOREIGN KEY (produto_id, estabelecimento_id)
        REFERENCES produtos(id, estabelecimento_id)
);

CREATE TABLE ajustes_estoque (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL,
    produto_id BIGINT NOT NULL,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    quantidade_anterior INTEGER NOT NULL,
    quantidade_nova INTEGER NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (produto_id, estabelecimento_id)
        REFERENCES produtos(id, estabelecimento_id),

    FOREIGN KEY (estabelecimento_id, usuario_id)
        REFERENCES estabelecimento_usuarios(estabelecimento_id, usuario_id)
);

CREATE INDEX idx_produtos_estabelecimento
    ON produtos(estabelecimento_id);

CREATE INDEX idx_estoques_produto
    ON estoques(produto_id);

CREATE INDEX idx_ajustes_produto_data
    ON ajustes_estoque(produto_id, criado_em DESC);
