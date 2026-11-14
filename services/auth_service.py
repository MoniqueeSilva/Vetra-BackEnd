from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
    InvalidHashError
)

from repositories.auth_repository import AuthRepository
password_hasher = PasswordHasher()

class AuthService:

    @staticmethod
    def autenticar(email, senha):

        if not isinstance(email, str) or not isinstance(senha, str):
            return None

        email = email.strip().lower()

        if not email or not senha:
            return None

        usuario = AuthRepository.buscar_por_email(email)

        if not usuario:
            return None

        try:
            password_hasher.verify(
                usuario["senha_hash"],
                senha
            )
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return None

        return {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "estabelecimento_id": usuario["estabelecimento_id"],
            "estabelecimento_nome": usuario["estabelecimento_nome"],
            "perfil": usuario["perfil"]
        }
