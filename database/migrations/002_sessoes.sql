CREATE TABLE sessoes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario_id BIGINT NOT NULL REFERENCES usuarios(id),
    estabelecimento_id BIGINT NOT NULL,
    token_hash VARCHAR(64) NOT NULL UNIQUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expira_em TIMESTAMPTZ NOT NULL,
    revogado_em TIMESTAMPTZ,

    FOREIGN KEY (estabelecimento_id, usuario_id)
        REFERENCES estabelecimento_usuarios(estabelecimento_id, usuario_id),

    CHECK (expira_em > criado_em)
);

CREATE INDEX idx_sessoes_usuario
    ON sessoes(usuario_id);

CREATE INDEX idx_sessoes_expiracao
    ON sessoes(expira_em);

CREATE INDEX idx_sessoes_token
    ON sessoes(token_hash);
