from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User():
    __tablename__='users'
    id=db.Column(db.Integer(),primary_key=True)
    password=db.Column(db.String(100))
    mail=db.Column(db.String(50))
    login=db.Column(db.String(50))
    albums = db.relationship('Album',backref='user')
    photos = db.relationship('Photo',backref='user')

    def __init__(self, login, mail, password):
        self.login = login
        self.password = password
        self.mail = mail
        

    @property
    def json(self):
        return self.__dict__


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    decor_css = db.Column(db.String(50), nullable=False)
    photos = db.relationship('Photo',backref='album')

    def __init__(self,id,name,user_id,decor_css):
        self.id=id
        self.name=name
        self.user_id=user_id
        self.decor_css=decor_css

    @property
    def json(self):
        return self.__dict__

class Photo(db.Model):
    __tablename__='photos'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    album_id = db.Column(db.Integer(), db.ForeignKey('albums.id'), nullable = False)
    path = db.Column(db.String(100), nullable = False)
    comment = db.Column(db.String(50))
    shot_date = db.Column(db.DateTime())

    def __init__(self, user_id, album_id, path, comment, shot_date=datetime.utcnow()):
        self.user_id = user_id
        self.album_id = album_id
        self.path = path
        self.comment = comment
        self.shot_date = shot_date

    @property
    def json(self):
        return self.__dict__