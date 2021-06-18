from flask import Blueprint

from similar_sticks.services import SaveDataService
from similar_sticks.models import Make, Stick, Curve, Flex


maintenance_pages = Blueprint('life_support', __name__, url_prefix='/life_support')


@maintenance_pages.route("/load_current_data/")
def load_data():
    save_data_service = SaveDataService()
    data = save_data_service.load_and_save_data()
    return {'result': data}


@maintenance_pages.route("/create_db/")
def create_db():
    from similar_sticks.models.base import setup_database
    setup_database()
    return {'result': 'success'}


@maintenance_pages.route("/get_makes/")
def get_makes():
    return {'result': {'makes': [make.name for make in Make.query.all()]}}


@maintenance_pages.route("/get_flexes/")
def get_flexes():
    return {'result': {'flexes': [flex.pounds for flex in Flex.query.all()]}}


@maintenance_pages.route("/get_curves/")
def get_curves():
    return {'result': {'curves': [curve.to_representation() for curve in Curve.query.all()]}}


@maintenance_pages.route("/get_sticks/")
def get_sticks():
    return {'result': {'sticks': [stick.to_representation() for stick in Stick.query.all()]}}
