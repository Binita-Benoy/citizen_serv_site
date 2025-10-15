from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models import BirthApplication, ApplicationStatus

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.post("")
@jwt_required()
def create_application():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
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
    return {"id": app.id, "status": app.status.value}, 201

@bp.get("")
@jwt_required()
def list_my_apps():
    user_id = get_jwt_identity()
    status = request.args.get("status")
    q = BirthApplication.query.filter_by(user_id=user_id)
    if status:
        q = q.filter(BirthApplication.status == ApplicationStatus(status))
    items = [{
        "id": a.id,
        "applicant_name": a.applicant_name,
        "status": a.status.value,
        "created_at": a.created_at.isoformat()
    } for a in q.order_by(BirthApplication.id.desc()).all()]
    return {"items": items}

@bp.get("/<int:app_id>")
@jwt_required()
def get_one(app_id: int):
    user_id = get_jwt_identity()
    a = BirthApplication.query.filter_by(id=app_id, user_id=user_id).first_or_404()
    return {
        "id": a.id,
        "applicant_name": a.applicant_name,
        "date_of_birth": a.date_of_birth.isoformat(),
        "place_of_birth": a.place_of_birth,
        "father_name": a.father_name,
        "mother_name": a.mother_name,
        "address": a.address,
        "status": a.status.value,
    }

@bp.put("/<int:app_id>")
@jwt_required()
def update_one(app_id: int):
    user_id = get_jwt_identity()
    a = BirthApplication.query.filter_by(id=app_id, user_id=user_id).first_or_404()
    if a.status != ApplicationStatus.pending:
        return {"msg": "Only PENDING applications can be updated"}, 400
    data = request.get_json() or {}
    for field in ["applicant_name", "place_of_birth", "father_name", "mother_name", "address"]:
        if field in data:
            setattr(a, field, data[field])
    db.session.commit()
    return {"msg": "updated"}

@bp.delete("/<int:app_id>")
@jwt_required()
def delete_one(app_id: int):
    user_id = get_jwt_identity()
    a = BirthApplication.query.filter_by(id=app_id, user_id=user_id).first_or_404()
    if a.status != ApplicationStatus.pending:
        return {"msg": "Only PENDING applications can be deleted"}, 400
    db.session.delete(a)
    db.session.commit()
    return {"msg": "deleted"}
