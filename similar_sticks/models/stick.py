from similar_sticks.models import db


curves = db.Table('curves',
                  db.Column('curve_id', db.Integer, db.ForeignKey('curve.id'), primary_key=True),
                  db.Column('stick_id', db.Integer, db.ForeignKey('stick.id'), primary_key=True)
                  )
flexes = db.Table('flexes',
                  db.Column('flex_id', db.Integer, db.ForeignKey('flex.pounds'), primary_key=True),
                  db.Column('stick_id', db.Integer, db.ForeignKey('stick.id'), primary_key=True)
                  )


class Stick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    model = db.Column(db.String(120))
    kickpoint = db.Column(db.String(25))

    make_id = db.Column(db.Integer, db.ForeignKey('make.id'), nullable=False)

    curves = db.relationship('Curve', secondary=curves, lazy='subquery', backref=db.backref('sticks', lazy=True))
    flexes = db.relationship('Flex', secondary=flexes, lazy='subquery', backref=db.backref('sticks', lazy=True))

    def to_representation(self):
        return {
            'id': self.id,
            'make': self.make.name,
            'year': self.year,
            'model': self.model,
            'kickpoint': self.kickpoint,
            'curves': [curve.name for curve in self.curves],
            'flexes': [flex.pounds for flex in self.flexes]
        }
