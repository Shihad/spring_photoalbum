from flask import Flask, request

from models import db, User, Album, Photo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you_cant_guess_this_key'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    user1 = User('vvasya','vasya.vasin@mail.com','qwerty')
    user2 = User('petya','pet.pyatochkin@mail.com','12345')
    user3 = User('olyalya','yaolya@mail.com','ytrewq')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

# Дмитрий
@app.route("/users")
def users():
    res = {"users": []}
    users = db.session.query(User).get_all()
    for user in users:
        res["users"].append(user.json)
    return res



@app.route("/albums")
def albums():
    res = {"albums": []}
    user_id = request.args["user_id"]
    albums = db.session.query(User).get(user_id=user_id)
    for album in albums:
        res["albums"].append(album.json)
    return res


@app.route("/photos")
def photos():
    res = {"photos": []}
    album_id = request.args["album_id"]
    photos = db.session.query(User).get(album_id=album_id)
    for photo in photos:
        res["photos"].append(photo.json)
    return res




app.run()
