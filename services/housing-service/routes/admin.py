from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..utils.security import role_required
from ..extensions import db
from ..models import HousingApplication

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/applications")
@jwt_required()
@role_required("admin")
def pending():
    apps = HousingApplication.query.filter_by(status="PENDING").all()
    return {"pending": [{"id": a.id, "applicant_name": a.applicant_name} for a in apps]}

@bp.post("/applications/<int:app_id>/decision")
@jwt_required()
@role_required("admin")
def decide(app_id):
    data = request.get_json()
    decision = (data.get("decision") or "").upper()
    if decision not in ["APPROVED", "REJECTED"]:
        return {"msg": "Invalid decision"}, 400
    app = HousingApplication.query.get_or_404(app_id)
    app.status = decision
    db.session.commit()
    return {"msg": f"Housing application {decision.lower()}"}
