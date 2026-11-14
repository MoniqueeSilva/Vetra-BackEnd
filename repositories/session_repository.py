from database.connection import get_connection

class SessionRepository:
    @staticmethod
    def criar(usuario_id, estabelecimento_id, token_hash, expira_em):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sessoes (
                        usuario_id,
                        estabelecimento_id,
                        token_hash,
                        expira_em
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """, (
                    usuario_id,
                    estabelecimento_id,
                    token_hash,
                    expira_em
                ))

                resultado = cursor.fetchone()

            conn.commit()
            return resultado["id"]

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def buscar_ativa(token_hash):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        u.id,
                        u.nome,
                        u.email,
                        eu.estabelecimento_id,
                        e.nome AS estabelecimento_nome,
                        eu.perfil
                    FROM sessoes s
                    INNER JOIN usuarios u
                        ON u.id = s.usuario_id
                    INNER JOIN estabelecimento_usuarios eu
                        ON eu.usuario_id = s.usuario_id
                        AND eu.estabelecimento_id = s.estabelecimento_id
                    INNER JOIN estabelecimentos e
                        ON e.id = s.estabelecimento_id
                    WHERE s.token_hash = %s
                      AND s.revogado_em IS NULL
                      AND s.expira_em > NOW()
                      AND u.ativo = TRUE
                      AND eu.ativo = TRUE
                      AND e.ativo = TRUE
                    LIMIT 1;
                """, (token_hash,))

                resultado = cursor.fetchone()
                return dict(resultado) if resultado else None

        finally:
            conn.close()

    @staticmethod
    def revogar(token_hash):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE sessoes
                    SET revogado_em = NOW()
                    WHERE token_hash = %s
                      AND revogado_em IS NULL;
                """, (token_hash,))

            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
