from similar_sticks.models import Stick, Curve, Flex, Make, db


class SearchDataService:

    def get_default_dropdowns(self):
        distinct_years = db.session.query(Stick.year.distinct().label('year'))
        years = [{'id': item.year, 'name': item.year} for item in distinct_years.all()]
        flexes = [flex.to_representation() for flex in Flex.query.all()]
        makes = [make.get_id_and_name() for make in Make.query.all()]
        curves = [curve.get_id_and_name() for curve in Curve.query.all()]

        return {'years': years, 'makes': makes, 'flexes': flexes, 'curves': curves}
