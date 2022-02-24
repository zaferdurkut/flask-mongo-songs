import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from api.common_controller import blueprint_common
from config.config import config

load_dotenv()
ENV = os.getenv("ENV", "default")

if ENV not in config:
    raise Exception("Invalid ENV: %s" % ENV)


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config.from_object(config[ENV]())
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register extensions."""
    pass


def register_blueprints(app):
    """Register blueprints."""
    app.register_blueprint(blueprint_common)
