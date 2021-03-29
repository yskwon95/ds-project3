from my_app import db

class City(db.model):#=> Base
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    cityname = db.Column(db.String(32))

    dusts = db.relationship("City", backref='city')

    def __repr__(self):
        return f"City {self.id}"

cities = City(cityname=['서울', '부산', '대구', '인천', '광주', '대전', '울산','경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종'])
db.session.add(cities)
db.session.commit()