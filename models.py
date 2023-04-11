from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Сделать User - Богдан
class User(db.Models):
    __tablename__='users'

#Сделать Album - Никита
class Albums(db.Model):
    __tablename__ = 'Albums'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    decor_css = db.Column(db.string(), nullable=False)
    def __init__(self,id,name.user_id,decor_css):
        self.id=id
        self.name=name
        self.user_id=user_id
        self.decor_css=decor_css



#Сделать Photo - Арсений
class Photo(db.Models):
    __tablename__='photos'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(50), nullable = False, db.ForeignKey('albums.id'))
    album_id = db.Column(db.String(50), nullable = False, db.ForeignKey('albums.id'))
    path = db.Column(db.String(100), nullable = False)
    comment = db.Column(db.String(50))
    shot_date = db.Column(db.Date)

    def __init__(self, user_id, album_id, path, comment, shot_date):
        self.user_id = user_id
        self.album_id = album_id
        self.path = path
        self.comment = comment
        self.shot_date = shot_date
