from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#импортировать werkzeug и хранить паролим в шифрованном виде
from werkzeug.security import check_password_hash, generate_password_hash
db = SQLAlchemy()

class User(db.Model):
    __tablename__= "db_users"
    id = db.Column(db.Integer(), primary_key=True)
    password=db.Column(db.String(100))
    mail=db.Column(db.String(50))
    login=db.Column(db.String(50))
    albums = db.relationship('Album',backref='user')
    photos = db.relationship('Photo',backref='user')

    def __init__(self, login, mail, password):
        self.login = login
        hash = generate_password_hash(password)
        self.password = hash
        self.mail = mail

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def json(self):
        dict = self.__dict__
        del(dict['_sa_instance_state'])
        del (dict['password'])
        return dict


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('db_users.id'), nullable=False)
    decor_css = db.Column(db.String(50), nullable=False)
    photos = db.relationship('Photo',backref='album')

    def __init__(self,name,user_id,decor_css="static/css/standart_photo.css"):
        self.name=name
        self.user_id=user_id
        self.decor_css=decor_css

    @property
    def json(self):
        dict = self.__dict__
        del (dict['_sa_instance_state'])
        return dict

class Photo(db.Model):
    __tablename__='photos'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('db_users.id'), nullable = False)
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
        dict = self.__dict__
        del (dict['_sa_instance_state'])
        return dict