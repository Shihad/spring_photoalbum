from flask import Flask, request

from models import db, User, Album, Photo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you_cant_guess_this_key'

db.init_app(app)


# Дмитрий
@app.route("/users")
def users():
    res = {"users": []}
    users = db.session.query(User).get_all()
    for user in users:
        res["users"].append(user.json)
    return res


    """
    В классе User нужен property json
    @property
    def json(self):
        return self.__dict__
    """


@app.route("/albums")
def albums():
    res = {"albums": []}
    user_id = request.args["user_id"]
    albums = db.session.query(User).get(user_id)
    for album in albums:
        res["albums"].append(album.json)
    return res

    """
    Запрос должен содержать argument user_id
    
    В классе Album нужен property json
    @property
    def json(self):
        return self.__dict__
    """

@app.route("/photos")
def photos():
    res = {"photos": []}
    album_id = request.args["album_id"]
    photos = db.session.query(User).get(album_id)
    for photo in photos:
        res["photos"].append(photo.json)
    return res


    """
    Запрос должен содержать argument album_id
    
    В классе Album нужен property json
    @property
    def json(self):
        return self.__dict__
    """


app.run()
