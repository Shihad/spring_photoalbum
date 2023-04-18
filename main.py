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
    db.session.commit()
    user1 = User('vvasya','vasya.vasin@mail.com','qwerty')
    user2 = User('petya','pet.pyatochkin@mail.com','12345')
    user3 = User('olyalya','yaolya@mail.com','ytrewq')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    album1 = Album('Море 2022', user1.id)
    db.session.add(album1)
    db.session.commit()

# Дмитрий
@app.route("/users", methods = ['post','get'])
def users():
    if request.method == "GET":
        res = {"users": []}
        userslist = db.session.query(User).all()
        for user in userslist:
            res["users"].append(user.json)
        return res
    if request.method == "POST":
        login = request.data['login']
        password = request.data['password']
        pass_confirm = request.data['pass_confirm']
        email = request.data['email']
        user = User.query.filter_by(login == login).first()
        if user:
            return {"error":"This login already registered"}
        user = User.query.filter_by(email == email).first()
        if user:
            return {"error": "This email already registered"}
        if pass_confirm!=password:
            return {"error": "Password not confirmed"}
        user = User(login,email,password)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created succesfully"}

@app.route("/users/<uid>")
def user_page(uid):
    #Богдан
    return

@app.route("/albums")
def albums():
    # Добавить проверку методов GET, POST, UPDATE, DELETE
    # Богдан
    res = {"albums": []}
    albumslist = db.session.query(Album).all()
    for album in albumslist:
        res["albums"].append(album.json)
    return res

@app.route("/albums/<aid>")
def album_page(aid):
    #Арсений
    return

@app.route("/photos")
def photos():
    #Добавить проверку методов GET, POST, UPDATE, DELETE
    #Никита
    res = {"photos": []}
    photoslist = db.session.query(Photo).all();
    for photo in photoslist:
        res["photos"].append(photo.json)
    return res

@app.route("/photos/<pid>")
def photo_page(pid):
    #Никита
    return



app.run()
