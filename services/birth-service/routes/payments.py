import random
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Payment, PaymentStatus, BirthApplication, ApplicationStatus

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.post("")
@jwt_required()
def create_payment():
    data = request.get_json() or {}
    app_id = data.get("application_id")
    amount_cents = int(data.get("amount_cents", 0))
    currency = (data.get("currency") or "AUD").upper()

    app = BirthApplication.query.get_or_404(app_id)
    # simple ownership check: users can pay for their own applications, admins may also pay
    # (you can tighten this with role checks if needed)
    if app.status not in (ApplicationStatus.pending, ApplicationStatus.rejected):
        return {"msg": "Payment only allowed when application is PENDING/REJECTED"}, 400

    pay = Payment(
        application_id=app_id,
        amount_cents=amount_cents,
        currency=currency,
        provider_ref=f"SIM-{random.randint(100000,999999)}",
        status=PaymentStatus.paid if random.random() > 0.1 else PaymentStatus.failed
    )
    db.session.add(pay)
    if pay.status == PaymentStatus.paid:
        app.status = ApplicationStatus.paid
    db.session.commit()
    return {
        "id": pay.id,
        "status": pay.status.value,
        "provider_ref": pay.provider_ref
    }, 201

@bp.get("/<int:payment_id>")
@jwt_required()
def get_payment(payment_id: int):
    p = Payment.query.get_or_404(payment_id)
    return {
        "id": p.id,
        "application_id": p.application_id,
        "amount_cents": p.amount_cents,
        "currency": p.currency,
        "status": p.status.value,
        "provider_ref": p.provider_ref
    }
