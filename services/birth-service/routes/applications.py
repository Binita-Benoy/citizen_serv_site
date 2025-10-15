from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import BirthApplication
from datetime import datetime

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.post("")
@jwt_required()
def create_application():
    user_id = get_jwt_identity()
    data = request.get_json()
    app = BirthApplication(
        user_id=user_id,
        applicant_name=data["applicant_name"],
        date_of_birth=datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date(),
        place_of_birth=data["place_of_birth"],
        father_name=data.get("father_name"),
        mother_name=data.get("mother_name"),
        address=data.get("address"),
    )
    db.session.add(app)
    db.session.commit()
    return {"id": app.id, "status": app.status}, 201

@bp.get("")
@jwt_required()
def list_applications():
    user_id = get_jwt_identity()
    apps = BirthApplication.query.filter_by(user_id=user_id).all()
    return {"applications": [
        {"id": a.id, "applicant_name": a.applicant_name, "status": a.status, "created_at": a.created_at.isoformat()}
        for a in apps
    ]}
