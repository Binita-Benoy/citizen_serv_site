import os
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import init_extensions, db
from .routes import auth as auth_routes
from .routes import applications as applications_routes
from .routes import admin as admin_routes
from .routes import payments as payments_routes

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    init_extensions(app)

    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(applications_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(payments_routes.bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    with app.app_context():
        db.create_all()  # Simple for teaching; Alembic can be added later
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), debug=True)
