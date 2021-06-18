import os
from flask import Flask

from similar_sticks.settings import set_settings
from similar_sticks.route_blueprints import viewer_pages, maintenance_pages
from similar_sticks.services import CsvDataService, SearchDataService


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    set_settings(app)
    app.search_data_service = SearchDataService()
    app.app_context().push()

    from similar_sticks.models import db
    db.init_app(app)
    db.create_all()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(viewer_pages)
    app.register_blueprint(maintenance_pages)

    return app
