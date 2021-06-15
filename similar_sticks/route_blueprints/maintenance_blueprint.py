from flask import Blueprint, current_app


maintenance_pages = Blueprint('life_support', __name__, url_prefix='/life_support')


@maintenance_pages.route("/load_current_data/")
def load_current_data():
    csv_service = current_app.config['CSV_DATA_SERVICE']
    current_data = csv_service.load_current_data()
    return {'result': current_data}


@maintenance_pages.route("/get_raw_data/")
def get_raw_data():
    csv_service = current_app.config['CSV_DATA_SERVICE']
    return {'result': csv_service.raw_stick_data}


@maintenance_pages.route("/get_formatted_data/")
def get_formatted_data():
    csv_service = current_app.config['CSV_DATA_SERVICE']
    return {'result': csv_service.formatted_stick_data}


@maintenance_pages.route("/get_unique_data/")
def get_unique_data():
    csv_service = current_app.config['CSV_DATA_SERVICE']
    return csv_service.get_unique_values()
