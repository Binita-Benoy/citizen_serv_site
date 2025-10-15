from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import init_extensions, db
from .routes import auth, applications, payments, admin

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(applications.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(admin.bp)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "VehicleRegistrationService"}

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5002, debug=True)
