from my_app import db

class Dust(db.Model):
    __tablename__ = 'dust'

    id = db.Column(db.Integer, primary_key=True)
    so2 = db.Column(db.Integer)
    co = db.Column(db.Integer)
    o3 = db.Column(db.Integer)
    no2 = db.Column(db.Integer)
    pm10 = db.Column(db.Integer)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    def __repr__(self):
        return f"Dust {self.id}"
