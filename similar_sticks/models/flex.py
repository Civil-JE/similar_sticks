from similar_sticks.models import db


class Flex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    def to_representation(self):
        return {
            'id': self.id,
            'name': self.name
        }
