from flask import current_app

from similar_sticks.services import CsvDataService
from similar_sticks.models import Stick, Curve, CurveNicknames, Flex, Make, db


class SaveDataService:
    def __init__(self):
        self.raw_stick_data = None
        self.raw_curve_data = None
        self.raw_flex_data = None
        self.raw_make_data = None
        # self.unique_years = set()
        # self.unique_makes = set()
        # self.unique_models = set()
        # self.unique_curves = set()
        # self.unique_kickpoints = set()

    def load_raw_data(self):
        csv_service = CsvDataService()
        data_path = current_app.config['STATIC_DATA_PATH']

        self.raw_stick_data = csv_service.load_raw_data(data_path+'stick_data.csv')
        self.raw_curve_data = csv_service.load_raw_data(data_path+'curve_data.csv')
        self.raw_flex_data = csv_service.load_raw_data(data_path+'flex_data.csv')
        self.raw_make_data = csv_service.load_raw_data(data_path+'make_data.csv')

    def save_flexes(self):
        db.session.bulk_save_objects(
            [Flex(id=int(flex), pounds=flex) for flex in self.raw_flex_data]
        )
        db.session.commit()

    def save_makes(self):
        db.session.add_all(
            [Make(name=make) for make in self.raw_make_data]
        )
        db.session.commit()

    def save_curves(self):
        pass

    def save_sticks(self):
        pass
