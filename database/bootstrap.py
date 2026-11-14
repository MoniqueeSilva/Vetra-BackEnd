from getpass import getpass

from argon2 import PasswordHasher

from database.connection import get_connection


password_hasher = PasswordHasher()


def criar_administrador():
    print("\n=== CONFIGURAÇÃO INICIAL DO VETRA ===\n")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # Impede duas configurações iniciais simultâneas.
            cursor.execute("SELECT pg_advisory_xact_lock(20261113)")

            cursor.execute("""
                SELECT
                    (SELECT COUNT(*) FROM estabelecimentos) AS estabelecimentos,
                    (SELECT COUNT(*) FROM usuarios) AS usuarios;
            """)

            estado = cursor.fetchone()

            if estado["estabelecimentos"] > 0 or estado["usuarios"] > 0:
                raise RuntimeError(
                    "O Vetra já possui dados iniciais. "
                    "A configuração inicial não pode ser repetida."
                )

            nome_estabelecimento = input(
                "Nome do estabelecimento: "
            ).strip()

            nome_usuario = input(
                "Nome do administrador: "
            ).strip()

            email = input(
                "E-mail do administrador: "
            ).strip().lower()

            senha = getpass("Senha do administrador: ")
            confirmacao = getpass("Confirme a senha: ")

            if not all([
                nome_estabelecimento,
                nome_usuario,
                email
            ]):
                raise ValueError("Todos os campos são obrigatórios.")

            if "@" not in email or "." not in email.split("@")[-1]:
                raise ValueError("Informe um e-mail válido.")

            if senha != confirmacao:
                raise ValueError("As senhas não coincidem.")

            if len(senha) < 12:
                raise ValueError(
                    "A senha precisa ter pelo menos 12 caracteres."
                )

            senha_hash = password_hasher.hash(senha)

            cursor.execute("""
                INSERT INTO estabelecimentos (nome)
                VALUES (%s)
                RETURNING id;
            """, (nome_estabelecimento,))

            estabelecimento_id = cursor.fetchone()["id"]

            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (nome_usuario, email, senha_hash))

            usuario_id = cursor.fetchone()["id"]

            cursor.execute("""
                INSERT INTO estabelecimento_usuarios
                    (estabelecimento_id, usuario_id, perfil)
                VALUES (%s, %s, 'ADM');
            """, (estabelecimento_id, usuario_id))

        conn.commit()

        print("\nAdministrador criado com sucesso!")
        print(f"Estabelecimento ID: {estabelecimento_id}")
        print(f"Usuário ID: {usuario_id}")
        print(f"E-mail: {email}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    criar_administrador()
