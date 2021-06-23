from operator import itemgetter
from flask import Blueprint, render_template, jsonify, request

from similar_sticks.models import Stick, Curve, Flex, Make
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

    sticks = Stick.query
    curves = Curve.query

    if year > 0:
        sticks = sticks.filter_by(year=year)

    if make_id > 0:
        sticks = sticks.filter_by(make_id=make_id)
        curves = curves.filter_by(make_id=make_id)

    if flex_id > 0:
        sticks = sticks.join(Stick.flexes, aliased=True).filter_by(id=flex_id)

    if curve_id > 0:
        sticks = sticks.join(Stick.curves, aliased=True).filter_by(id=curve_id)

    result = {'sticks': [stick.to_representation() for stick in sticks.all()],
              'curves': [curve.to_representation() for curve in curves.all()]}

    return jsonify(result)


@search_pages.route("/update_from_text_search", methods=['POST'])
def update_from_text_search():
    req = request.json
    search_items = req.get('search_text').split(' ')

    if req.get('current_sticks')[0] == '-1':
        current_sticks = []
    else:
        current_sticks = [int(item) for item in req.get('current_sticks')]

    # If we have a list of sticks in the results already, search based off those
    if current_sticks:
        sticks = Stick.query.filter(Stick.id.in_(current_sticks))
    else:
        sticks = Stick.query

    match_sticks = []
    for stick in sticks:
        match_count = 0
        for search_item in search_items:
            match_count += stick.search_string.count(search_item.upper())
        if match_count:
            match_sticks.append((match_count, stick.to_representation()))

    if match_sticks:
        match_sticks.sort(key=itemgetter(0), reverse=True)
        result = {'sticks': [match[1] for match in match_sticks[:10]]}  # Just want the top ten results
    else:
        result = {'sticks': []}

    return jsonify(result)


@search_pages.route("/get_default_dropdown_values", methods=['POST'])
def get_default_dropdown_values():
    search_data_service = SearchDataService()
    default_values = search_data_service.get_default_dropdowns()
    return jsonify(default_values)
