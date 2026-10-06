from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.ext import db
from app.models.user import User
from app.utils.decorators import role_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    dados = request.get_json(silent=True) or {}

    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not nome or not email or not senha:
        return jsonify(erro="nome, email e senha são obrigatórios"), 400

    if len(senha) < 8:
        return jsonify(erro="a senha deve ter pelo menos 8 caracteres"), 400

    if User.query.filter_by(email=email).first():
        return jsonify(erro="email já cadastrado"), 409

    user = User(
        nome=nome,
        email=email,
        senha_hash=generate_password_hash(senha),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(id=user.id, nome=user.nome, email=user.email, role=user.role), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha:
        return jsonify(erro="email e senha são obrigatórios"), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.senha_hash, senha):
        return jsonify(erro="email ou senha inválidos"), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
    )

    return jsonify(access_token=token), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))

    if not user:
        return jsonify(erro="usuário não encontrado"), 404

    return jsonify(id=user.id, nome=user.nome, email=user.email, role=user.role), 200


@auth_bp.route("/admin-teste", methods=["GET"])
@role_required("ADMIN")
def admin_teste():
    return jsonify(mensagem="você é admin"), 200