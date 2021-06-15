import os
from flask import Flask

from similar_sticks.settings import set_settings
from similar_sticks.route_blueprints import viewer_pages, maintenance_pages
from similar_sticks.services import CsvDataService


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    set_settings(app)
    app.config['CSV_DATA_SERVICE'] = CsvDataService(app.config['STICK_DATA_PATH'])

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(viewer_pages)
    app.register_blueprint(maintenance_pages)

    return app
