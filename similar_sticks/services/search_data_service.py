from operator import itemgetter
from collections import Counter

from similar_sticks.models import Stick, Curve, Flex, Make, db


class SearchDataService:

    def get_default_dropdowns(self):
        distinct_years = db.session.query(Stick.year.distinct().label('year'))
        years = [{'id': item.year, 'name': item.year} for item in distinct_years.all()]
        flexes = [flex.to_representation() for flex in Flex.query.all()]
        makes = [make.get_id_and_name() for make in Make.query.all()]
        curves = [curve.get_id_and_name() for curve in Curve.query.all()]

        return {'years': years, 'makes': makes, 'flexes': flexes, 'curves': curves}

    def get_results_from_dropdown(self, year, make_id, flex_id, curve_id):
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

        return result

    def get_results_from_search_items(self, search_items, current_sticks):
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
            return {'sticks': [match[1] for match in match_sticks[:10]]}  # Just want the top ten results
        else:
            return {'sticks': []}

    def get_comparable_sticks(self, stick, flex, curve):
        comparable_sticks = Stick.query

        similar_curves = [curve.id for curve in self.compare_curves(curve)]

        comparable_sticks = comparable_sticks.filter_by(kickpoint=stick.kickpoint)
        comparable_sticks = comparable_sticks.join(Stick.flexes, aliased=True).filter_by(id=flex.id)
        comparable_sticks = comparable_sticks.join(Stick.curves, aliased=True).filter(Curve.id.in_(similar_curves))

        return {'sticks': [comparable_stick.to_representation() for comparable_stick in comparable_sticks]}

    def compare_curves(self, selected_curve):
        curves = Curve.query

        curve_type_matches = curves.filter_by(curve_type=selected_curve.curve_type)
        face_type_matches = curves.filter_by(face_type=selected_curve.face_type)
        depth_matches = curves.filter_by(depth=selected_curve.depth)
        toe_type_matches = curves.filter_by(toe_type=selected_curve.toe_type)
        lie_matches = curves.filter_by(lie=selected_curve.lie)
        length_matches = curves.filter_by(length=selected_curve.length)

        all_matches = curve_type_matches.all() + face_type_matches.all() + depth_matches.all() \
            + toe_type_matches.all() + lie_matches.all() + length_matches.all()

        match_counter = Counter(all_matches)
        # Get the 5 most similar curves, take less if they match less than 3 values. This includes
        # the original curve.
        best_matches = [curve for curve, count in match_counter.most_common(5) if count >= 3]
        return best_matches
