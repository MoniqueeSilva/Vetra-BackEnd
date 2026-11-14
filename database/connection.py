import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


BACKEND_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BACKEND_DIR / ".env")


def get_connection():
    variaveis_obrigatorias = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    ausentes = [
        variavel
        for variavel in variaveis_obrigatorias
        if not os.getenv(variavel)
    ]

    if ausentes:
        raise RuntimeError(
            "Variáveis de ambiente não configuradas: "
            + ", ".join(ausentes)
        )

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
        connect_timeout=10,
        application_name="Vetra"
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'America/Sao_Paulo';")

        return conn

    except Exception:
        conn.close()
        raise


def test_connection():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    1 AS status,
                    CURRENT_DATABASE() AS database,
                    CURRENT_TIMESTAMP AS horario;
            """)

            return cursor.fetchone()

    finally:
        conn.close()
