import os
from dotenv import load_dotenv
from flask import Flask
from app.ext import db
from app.routes.main import main_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(main_bp)

    return app