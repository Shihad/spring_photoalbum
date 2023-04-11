from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Сделать User - Богдан
class User(db.Models):
    __tablename__='users'

#Сделать Album - Никита
class Album(db.Models):
    __tablename__='albums'

#Сделать Photo - Арсений
class Photo(db.Models):
    __tablename__='photos'