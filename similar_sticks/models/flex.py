from similar_sticks.models import db


class Flex(db.Model):
    pounds = db.Column(db.Integer, primary_key=True)
