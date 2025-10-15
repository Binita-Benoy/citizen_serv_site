from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import VehicleApplication
from datetime import datetime

bp = Blueprint("applications", __name__, url_prefix="/applications")

@bp.post("")
@jwt_required()
def create_app():
    user_id = get_jwt_identity()
    data = request.get_json()
    app = VehicleApplication(
        user_id=user_id,
        plate_number=data["plate_number"],
        vin=data["vin"],
        vehicle_type=data["vehicle_type"],
        owner_name=data["owner_name"]
    )
    db.session.add(app)
    db.session.commit()
    return {"id": app.id, "status": app.status}, 201

@bp.get("")
@jwt_required()
def list_apps():
    user_id = get_jwt_identity()
    apps = VehicleApplication.query.filter_by(user_id=user_id).all()
    return {"applications": [
        {"id": a.id, "plate_number": a.plate_number, "status": a.status, "created_at": a.created_at.isoformat()}
        for a in apps
    ]}

@bp.get("/<int:app_id>")
@bp.put("/<int:app_id>")
def detail_update_app(app_id):
    # you can follow the same pattern as birth: check ownership, allow update when PENDING, etc.
    pass
