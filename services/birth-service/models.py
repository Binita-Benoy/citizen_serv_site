from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class Role(Enum):
    user = "user"
    admin = "admin"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.user, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str):
        # Werkzeug’s helpers are simple and fine for starter projects
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class ApplicationStatus(Enum):
    pending = "PENDING"
    approved = "APPROVED"
    rejected = "REJECTED"
    paid = "PAID"

class BirthApplication(db.Model):
    __tablename__ = "birth_applications"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    applicant_name = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    place_of_birth = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(200))
    mother_name = db.Column(db.String(200))
    address = db.Column(db.Text)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.pending, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class PaymentStatus(Enum):
    initiated = "INITIATED"
    paid = "PAID"
    failed = "FAILED"
    refunded = "REFUNDED"

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.BigInteger, primary_key=True)
    application_id = db.Column(db.BigInteger, db.ForeignKey("birth_applications.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    amount_cents = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="AUD")
    provider_ref = db.Column(db.String(64))
    status = db.Column(db.Enum(PaymentStatus), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
