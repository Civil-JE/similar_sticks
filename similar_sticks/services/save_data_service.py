from flask import current_app

from similar_sticks.services import CsvDataService
from similar_sticks.models import Stick, Curve, CurveNicknames, Flex, Make, db


class SaveDataService:
    def __init__(self):
        self.raw_stick_data = None
        self.raw_curve_data = None
        self.raw_flex_data = None
        self.raw_make_data = None

    def load_and_save_data(self):
        self._load_raw_data()
        flexes = self._save_flexes()
        makes = self._save_makes()
        curves = self._save_curves()
        sticks = self._save_sticks()
        return {'flexes': len(flexes), 'makes': len(makes), 'curves': len(curves), 'sticks': len(sticks)}

    def _load_raw_data(self):
        csv_service = CsvDataService()
        data_path = current_app.config['STATIC_DATA_PATH']

        self.raw_stick_data = csv_service.load_raw_data(data_path+'stick_data.csv')
        self.raw_curve_data = csv_service.load_raw_data(data_path+'curve_data.csv')
        self.raw_flex_data = csv_service.load_raw_data(data_path+'flex_data.csv')
        self.raw_make_data = csv_service.load_raw_data(data_path+'make_data.csv')

    def _save_flexes(self):
        flexes = [Flex(pounds=int(flex[0])) for flex in self.raw_flex_data]
        db.session.bulk_save_objects(flexes)
        db.session.commit()
        return flexes

    def _save_makes(self):
        makes = [Make(name=make[0]) for make in self.raw_make_data]
        db.session.add_all(makes)
        db.session.commit()
        return makes

    def _save_curves(self):
        curves = list()
        nicknames = list()
        i = 1
        for raw_curve in self.raw_curve_data:
            curves.append(
                Curve(
                    id=i,
                    name=raw_curve[0],
                    make_id=Make.query.filter_by(name=raw_curve[1].upper()).first().id,
                    curve_type=raw_curve[2],
                    face_type=raw_curve[3],
                    toe_type=raw_curve[4],
                    lie=raw_curve[5],
                    length=raw_curve[6]
                )
            )
            raw_nicknames = raw_curve[7].strip('[]').split(',')
            nicknames.extend([CurveNicknames(nickname=nickname, curve_id=i) for nickname in raw_nicknames])
            i += 1

        db.session.add_all(curves+nicknames)
        db.session.commit()
        return curves

    def _save_sticks(self):
        sticks = list()
        for stick in self.raw_stick_data:
            make = Make.query.filter_by(name=stick[1].upper()).first()
            new_stick = Stick(
                year=stick[0],
                make_id=make.id,
                model=stick[2],
                kickpoint=stick[4],
                search_string=stick[0] + ' ' + make.name + ' ' + stick[2]
            )
            raw_curves = stick[3].strip('[]').split(',')
            raw_flexes = stick[5].strip('[]').split(',')
            new_stick.curves.extend(Curve.query.filter(Curve.name.in_([curve for curve in raw_curves])).all())
            new_stick.flexes.extend(Flex.query.filter(Flex.pounds.in_([int(flex) for flex in raw_flexes])).all())
            sticks.append(new_stick)

        db.session.add_all(sticks)
        db.session.commit()

        return sticks
