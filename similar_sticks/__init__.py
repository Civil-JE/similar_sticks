import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

from similar_sticks.settings import set_settings
from similar_sticks.route_blueprints import search_pages, maintenance_pages
from similar_sticks.services import CsvDataService, SearchDataService


csrf = CSRFProtect()
load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    set_settings(app)
    app.app_context().push()

    from similar_sticks.models import db
    db.init_app(app)
    db.create_all()

    csrf.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(search_pages)
    app.register_blueprint(maintenance_pages)

    return app
