from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/register")
def register():
    data = request.get_json() or {}
    if not data.get("email") or not data.get("password"):
        return {"msg": "Missing fields"}, 400
    if User.query.filter_by(email=data["email"]).first():
        return {"msg": "Email exists"}, 400
    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return {"msg": "User created"}, 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password")):
        return {"msg": "Bad credentials"}, 401
    token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    return jsonify(access_token=token, role=user.role)
