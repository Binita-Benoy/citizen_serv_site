from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import BirthApplication, ApplicationStatus
from ..utils.security import role_required

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/applications/pending")
@jwt_required()
@role_required("admin")
def pending():
    items = BirthApplication.query.filter_by(status=ApplicationStatus.pending).order_by(BirthApplication.id.desc()).all()
    return {"items": [{"id": a.id, "applicant_name": a.applicant_name} for a in items]}

@bp.post("/applications/<int:app_id>/decision")
@jwt_required()
@role_required("admin")
def decide(app_id: int):
    data = request.get_json() or {}
    decision = (data.get("decision") or "").upper()
    if decision not in {"APPROVED", "REJECTED"}:
        return {"msg": "decision must be APPROVED or REJECTED"}, 400
    a = BirthApplication.query.filter_by(id=app_id, status=ApplicationStatus.pending).first_or_404()
    a.status = ApplicationStatus.approved if decision == "APPROVED" else ApplicationStatus.rejected
    db.session.commit()
    return {"msg": f"{decision.lower()} ok"}
