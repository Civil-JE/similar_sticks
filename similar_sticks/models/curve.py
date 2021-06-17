from similar_sticks.models import db


class Curve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    curve_type = db.Column(db.String(50))
    face_type = db.Column(db.String(50))
    toe_type = db.Column(db.String(50))
    lie = db.Column(db.String(5))
    length = db.Column(db.String(50))
    nicknames = db.relationship('CurveNicknames', backref='curve', lazy=True)
    make_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)


class CurveNicknames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50))
    curve_id = db.Column(db.Integer, db.ForeignKey('curve.id'), nullable=False)
