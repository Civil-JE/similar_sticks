from similar_sticks.models import db


class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    curves = db.relationship('Curve', backref='make', lazy=True)
    sticks = db.relationship('Stick', backref='make', lazy=True)

    def to_representation(self):
        return {
            'id': self.id,
            'name': self.name,
            'curves': [curve.id for curve in self.curves],
            'sticks': [stick.id for stick in self.sticks]
        }

    def get_id_and_name(self):
        return {
            'id': self.id,
            'name': self.name
        }