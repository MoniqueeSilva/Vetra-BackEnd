from database.connection import get_connection

class AuthRepository:

    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        u.id,
                        u.nome,
                        u.email,
                        u.senha_hash,
                        eu.estabelecimento_id,
                        e.nome AS estabelecimento_nome,
                        eu.perfil
                    FROM usuarios u
                    INNER JOIN estabelecimento_usuarios eu
                        ON eu.usuario_id = u.id
                    INNER JOIN estabelecimentos e
                        ON e.id = eu.estabelecimento_id
                    WHERE LOWER(u.email) = LOWER(%s)
                      AND u.ativo = TRUE
                      AND eu.ativo = TRUE
                      AND e.ativo = TRUE
                    ORDER BY eu.estabelecimento_id
                    LIMIT 1;
                """, (email,))

                usuario = cursor.fetchone()

                return dict(usuario) if usuario else None

        finally:
            conn.close()
