import random
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Payment, HousingApplication

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.post("")
@jwt_required()
def pay():
    data = request.get_json()
    app_id = data.get("application_id")
    app = HousingApplication.query.get_or_404(app_id)
    pay = Payment(
        application_id=app_id,
        amount_cents=data.get("amount_cents", 15000),
        currency=data.get("currency", "AUD"),
        provider_ref=f"HSPAY-{random.randint(10000,99999)}",
        status="PAID"
    )
    app.status = "PAID"
    db.session.add(pay)
    db.session.commit()
    return {"payment_id": pay.id, "status": pay.status}
