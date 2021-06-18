from similar_sticks.models import db


class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    curves = db.relationship('Curve', backref='make', lazy=True)
    sticks = db.relationship('Stick', backref='make', lazy=True)
