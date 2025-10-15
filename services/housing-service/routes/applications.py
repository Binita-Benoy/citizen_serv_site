from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import HousingApplication

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.post("")
@jwt_required()
def create_app():
    uid = get_jwt_identity()
    data = request.get_json()
    app = HousingApplication(
        user_id=uid,
        applicant_name=data["applicant_name"],
        address=data["address"],
        household_size=data["household_size"],
        income_band=data["income_band"]
    )
    db.session.add(app)
    db.session.commit()
    return {"id": app.id, "status": app.status}, 201

@bp.get("")
@jwt_required()
def list_apps():
    uid = get_jwt_identity()
    apps = HousingApplication.query.filter_by(user_id=uid).all()
    return {"applications": [
        {"id": a.id, "address": a.address, "status": a.status, "created_at": a.created_at.isoformat()}
        for a in apps
    ]}
