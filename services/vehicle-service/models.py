from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class VehicleApplication(db.Model):
    __tablename__ = "vehicle_applications"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plate_number = db.Column(db.String(50), nullable=False)
    vin = db.Column(db.String(100), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    owner_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum('PENDING','APPROVED','REJECTED','PAID'), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.BigInteger, primary_key=True)
    application_id = db.Column(db.BigInteger, db.ForeignKey("vehicle_applications.id", ondelete="CASCADE"), nullable=False, index=True)
    amount_cents = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), default='AUD')
    provider_ref = db.Column(db.String(64))
    status = db.Column(db.Enum('INITIATED','PAID','FAILED','REFUNDED'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
