from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.ext import db
from app.models.user import User
from app.models.service import service
from app.utils.decorators import role_required
from sqlalchemy import select
from decimal import Decimal



serv_bp = Blueprint("serv", __name__)


@serv_bp.route("/consult", methods=["GET"])
@jwt_required()

def lista():
    consulta = select(service).where(service.ativo == True)
    resultado = db.session.scalars(consulta).all()
    
    if not resultado:
        return jsonify(erro="Serviço não encontrado"), 200
    
    
    return jsonify([i.to_dict() for i in resultado])


@serv_bp.route("/add", methods=["POST"])
@role_required("ADMIN")
def create():
    
    dados = request.get_json(silent=True) or {}
    
    nome = (dados.get("nome") or "").strip()
    preco = (dados.get("preco") or dados.get("preço") or "" )
    duracao =(dados.get("duracao") or dados.get("duração") or "")
    
   
    if not nome or not preco or not duracao:
        return jsonify(erro="nome, preço e duração são obrigatorios"), 400
    
    if preco <= 0 or duracao <= 0:
        return jsonify(erro="preco e duracao precisam ser maiores que zero")
    
    try:
         preco = Decimal(preco)
        
    except:
        return jsonify(erro="erro ao transformar preco em decimal")
        
    
    if isinstance(duracao, bool) or not isinstance(duracao, int):
        return jsonify(erro="duracao precisa ser um numero inteiro")
        
        
    
    if service.query.filter_by(nome=nome).first():
        return jsonify(erro="Serviço ja cadastrado"), 409
    
    Service = service(
        nome=nome,
        preco=preco,
        duracao=duracao,
    )
    
     
    db.session.add(Service)
    db.session.commit()
    
    return jsonify(Service.to_dict()), 201

    
    
    
