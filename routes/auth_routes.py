from flask import Blueprint, request, jsonify, make_response
from services.auth_service import AuthService
from services.session_service import SessionService

auth_bp = Blueprint("auth", __name__)

COOKIE_SESSAO = "vetra_session"
TEMPO_SESSAO_SEGUNDOS = 8 * 60 * 60

@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({
            "success": False,
            "message": "Dados da requisição inválidos."
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    usuario = AuthService.autenticar(email, senha)

    if not usuario:
        return jsonify({
            "success": False,
            "message": "E-mail ou senha inválidos."
        }), 401

    token = SessionService.criar(usuario)

    resposta = make_response(jsonify({
        "success": True,
        "message": "Login realizado com sucesso.",
        "usuario": usuario
    }), 200)

    resposta.set_cookie(
        COOKIE_SESSAO,
        token,
        max_age=TEMPO_SESSAO_SEGUNDOS,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/"
    )

    return resposta

@auth_bp.route("/me", methods=["GET"])
def verificar_sessao():

    token = request.cookies.get(COOKIE_SESSAO)
    usuario = SessionService.buscar(token)

    if not usuario:
        return jsonify({
            "success": False,
            "message": "Sessão inválida ou expirada."
        }), 401

    return jsonify({
        "success": True,
        "usuario": usuario
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():

    token = request.cookies.get(COOKIE_SESSAO)

    SessionService.encerrar(token)

    resposta = make_response(jsonify({
        "success": True,
        "message": "Sessão encerrada."
    }), 200)

    resposta.delete_cookie(
        COOKIE_SESSAO,
        path="/",
        httponly=True,
        secure=False,
        samesite="Lax"
    )

    return resposta
