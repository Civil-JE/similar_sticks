from similar_sticks.models import Stick, Curve, Flex, Make


class SearchDataService:

    def get_default_dropdowns(self):
        years = [{'id': year, 'name': year} for year in set([stick.year for stick in Stick.query.all()])]
        flexes = [flex.to_representation() for flex in Flex.query.all()]
        makes = [make.get_id_and_name() for make in Make.query.all()]
        curves = [curve.get_id_and_name() for curve in Curve.query.all()]

        return {'years': years, 'makes': makes, 'flexes': flexes, 'curves': curves}
