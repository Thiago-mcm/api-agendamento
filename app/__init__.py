import os
from dotenv import load_dotenv
from flask import Flask
from app.ext import db
from app.routes import init_routes

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    init_routes(app)

    return app