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
        flexes = [Flex(id=int(flex[0]), name=flex[0]) for flex in self.raw_flex_data]
        db.session.bulk_save_objects(flexes)
        db.session.commit()
        return flexes

    def _save_makes(self):
        makes = [Make(name=make[0]) for make in self.raw_make_data]
        db.session.add_all(makes)
        db.session.commit()
        return makes

    def _save_makes_from_curves(self, make_data):
        current_makes = Make.query
        new_makes = list()
        for make in make_data:
            if current_makes.filter_by(name=make).count() == 0:
                new_makes.append(Make(name=make))

        db.session.add_all(new_makes)
        db.session.commit()
        return new_makes

    def _save_curves(self):
        curves = list()
        nicknames = list()
        i = 1
        makes = list(set([curve[1] for curve in self.raw_curve_data]))
        self._save_makes_from_curves(makes)

        for raw_curve in self.raw_curve_data:
            make_query = Make.query.filter_by(name=raw_curve[1].upper())
            make_id = make_query.first().id if make_query.count() == 1 else Make.query.get(0)
            curves.append(
                Curve(
                    id=i,
                    name=raw_curve[0],
                    make_id=make_id,
                    curve_type=raw_curve[2],
                    face_type=raw_curve[3],
                    depth=raw_curve[3],
                    toe_type=raw_curve[5],
                    lie=raw_curve[6],
                    length=raw_curve[7]
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
            search_string = stick[0] + ' ' + make.name + ' ' + stick[2]
            new_stick = Stick(
                year=stick[0],
                make_id=make.id,
                model=stick[2],
                kickpoint=stick[4],
                search_string=search_string.upper()
            )
            raw_curves = stick[3].strip('[]').split(',')
            raw_flexes = stick[5].strip('[]').split(',')
            new_stick.curves.extend(Curve.query.filter(Curve.name.in_([curve for curve in raw_curves])).all())
            new_stick.flexes.extend(Flex.query.filter(Flex.id.in_([int(flex) for flex in raw_flexes])).all())
            sticks.append(new_stick)

        db.session.add_all(sticks)
        db.session.commit()

        return sticks
