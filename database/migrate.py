
from pathlib import Path
import re

from database.connection import get_connection


MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def executar_migracoes():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL UNIQUE,
                    aplicado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)
            conn.commit()

        arquivos = sorted(MIGRATIONS_DIR.glob("*.sql"))

        if not arquivos:
            print("Nenhuma migração encontrada.")
            return

        for arquivo in arquivos:
            if not re.fullmatch(r"\d+_[a-zA-Z0-9_-]+\.sql", arquivo.name):
                raise ValueError(
                    f"Nome de migração inválido: {arquivo.name}"
                )

            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM schema_migrations WHERE nome = %s",
                    (arquivo.name,)
                )

                if cursor.fetchone():
                    print(f"[IGNORADA] {arquivo.name} já foi aplicada.")
                    continue

                sql = arquivo.read_text(encoding="utf-8")

                try:
                    cursor.execute(sql)
                    cursor.execute(
                        "INSERT INTO schema_migrations (nome) VALUES (%s)",
                        (arquivo.name,)
                    )
                    conn.commit()

                    print(f"[OK] Migração aplicada: {arquivo.name}")

                except Exception:
                    conn.rollback()
                    raise

        print("Processo de migração concluído.")

    finally:
        conn.close()


if __name__ == "__main__":
    executar_migracoes()
