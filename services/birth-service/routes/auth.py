from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models import User, Role

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    role = data.get("role", "user")
    if not email or not password:
        return {"msg": "email and password required"}, 400
    if User.query.filter_by(email=email).first():
        return {"msg": "email already registered"}, 409
    user = User(email=email, role=Role(role))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"msg": "registered"}, 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"msg": "invalid credentials"}, 401
    token = create_access_token(identity=user.id, additional_claims={"role": user.role.value})
    return jsonify(access_token=token, role=user.role.value)
