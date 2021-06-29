from flask import Blueprint, render_template, jsonify, request

from similar_sticks.services import SearchDataService


search_pages = Blueprint('viewer_pages', __name__)


@search_pages.route("/")
def main_search():
    search_data_service = SearchDataService()
    default_values = search_data_service.get_default_dropdowns()
    return render_template('base.html', years=default_values['years'], flexes=default_values['flexes'],
                           makes=default_values['makes'], curves=default_values['curves'])


@search_pages.route("/update_from_dropdown", methods=['POST'])
def update_from_dropdown():
    req = request.json
    year = int(req.get('year')) if req.get('year') else 0
    make_id = int(req.get('make_id')) if req.get('make_id') else 0
    flex_id = int(req.get('flex_id')) if req.get('flex_id') else 0
    curve_id = int(req.get('curve_id')) if req.get('curve_id') else 0

    search_data_service = SearchDataService()

    return jsonify(search_data_service.get_results_from_dropdown(year, make_id, flex_id, curve_id))


@search_pages.route("/update_from_text_search", methods=['POST'])
def update_from_text_search():
    req = request.json
    search_items = req.get('search_text').split(' ')
    current_sticks = [int(item) for item in req.get('current_sticks')] if req.get('current_sticks')[0] == '-1' else []

    search_data_service = SearchDataService()

    return jsonify(search_data_service.get_results_from_search_items(search_items, current_sticks))


@search_pages.route("/get_default_dropdown_values", methods=['POST'])
def get_default_dropdown_values():
    search_data_service = SearchDataService()
    default_values = search_data_service.get_default_dropdowns()
    return jsonify(default_values)


@search_pages.route("/get_default_dropdown_values", methods=['POST'])
def get_comparable_sticks():
    pass
