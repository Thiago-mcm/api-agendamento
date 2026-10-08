from decimal import Decimal, InvalidOperation
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from app.ext import db
from app.models.service import Service
from app.utils.decorators import role_required

serv_bp = Blueprint("serv", __name__)


@serv_bp.route("/consult", methods=["GET"])
@jwt_required()
def lista():
    consulta = (
        select(Service)
        .where(Service.ativo.is_(True))
        .order_by(Service.nome)
    )
    resultado = db.session.scalars(consulta).all()

    return jsonify([i.to_dict() for i in resultado]), 200


@serv_bp.route("/<int:servico_id>", methods=["GET"])
@jwt_required()
def listar_servico(servico_id):
   
        
    consult = select(Service).where(Service.ativo == True).where(Service.id == servico_id)    
        
    resultado = db.session.scalar(consult)
    
    if not resultado:
        return jsonify(erro="Serviço não encontrado"), 404
    
        
    return jsonify(resultado.to_dict()), 200
    

@serv_bp.route("/add", methods=["POST"])
@role_required("ADMIN")
def create():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    preco = dados.get("preco") or dados.get("preço") or ""
    duracao = dados.get("duracao") or dados.get("duração") or ""

    if not isinstance(nome, str) or not nome.strip() or not preco or not duracao:
        return jsonify(erro="nome, preço e duração são obrigatórios"), 400

    nome = nome.strip()

    if len(nome) > 100:
        return jsonify(erro="nome deve ter no máximo 100 caracteres"), 400

    if isinstance(duracao, bool) or not isinstance(duracao, int) or duracao <= 0:
        return jsonify(erro="duracao deve ser um inteiro maior que zero"), 400

    try:
        preco = Decimal(str(preco))
    except InvalidOperation:
        return jsonify(erro="preco deve ser um número"), 400

    if not preco.is_finite() or preco <= 0 or preco >= 100000:
        return jsonify(erro="preco deve ser maior que zero e menor que 100000"), 400

    if Service.query.filter_by(nome=nome).first():
        return jsonify(erro="serviço já cadastrado"), 409

    novo = Service(nome=nome, preco=preco, duracao=duracao)

    db.session.add(novo)
    db.session.commit()

    return jsonify(novo.to_dict()), 201