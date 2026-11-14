import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from repositories.session_repository import SessionRepository


TEMPO_SESSAO_HORAS = 8


class SessionService:

    @staticmethod
    def gerar_hash(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def criar(usuario):
        token = secrets.token_urlsafe(32)

        token_hash = SessionService.gerar_hash(token)

        expira_em = (
            datetime.now(timezone.utc)
            + timedelta(hours=TEMPO_SESSAO_HORAS)
        )

        SessionRepository.criar(
            usuario_id=usuario["id"],
            estabelecimento_id=usuario["estabelecimento_id"],
            token_hash=token_hash,
            expira_em=expira_em
        )

        return token

    @staticmethod
    def buscar(token):
        if not token:
            return None

        token_hash = SessionService.gerar_hash(token)

        return SessionRepository.buscar_ativa(token_hash)

    @staticmethod
    def encerrar(token):
        if not token:
            return

        token_hash = SessionService.gerar_hash(token)

        SessionRepository.revogar(token_hash)
