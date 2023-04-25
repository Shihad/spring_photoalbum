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
    photo1 = Photo(user1.id, album1.id, "/static/img/1.jpg","Мы с Серегой")
    db.session.add(photo1)
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
        print(request.json)
        login = request.json['login']
        password = request.json['password']
        pass_confirm = request.json['pass_confirm']
        email = request.json['email']
        user = User.query.filter_by(login = login).first()
        if user:
            return {"error":"This login already registered"}
        user = User.query.filter_by(mail = email).first()
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
    #Богдан - изменить
    if request.method == "GET":
        pass
    if request.method == "PUT":
        login = request.json['login']
        #user = pass#найти в БД с указанным mail
        #user.login = login
        return
    if request.method == "DELETE":
        pass

@app.route("/albums", methods = ['post','get'])
def albums():
    # Добавить проверку методов GET, POST, UPDATE, DELETE
    # Богдан data заменить на json
    if request.method == "GET":
        res = {"albums": []}
        albumslist = db.session.query(Album).all()
        for album in albumslist:
            res["albums"].append(album.json)
        return res
    if request.method == "POST":
        name = request.data['name']
        user_id = request.data['']
        album = Album(name, user_id)
        db.session.add(album)
        db.session.commit()
    if request.method == "DELETE":
        #найти альбом
        db.session.delete(album)
        db.session.commit()
    if request.method == "UPDATE":
        pass

@app.route("/albums/<aid>",methods = ['GET','PUT', "DELETE"])
def album_page(aid):
    #Арсений
    if request.method == "GET":
        album=Album.query.filter_by(id=aid).first()
        print(album.name, 'имя')
        name=album.name
        print(album.user_id,'айди пользователя')
        user_id=album.user_id
        print(album.decor_css, "css")
        decor_css = album.decor_css
        print(album.photos,"фото")
        photos=album.photos
        print(album.name, album.user_id, album.decor_css, album.photos)
        res=[name, user_id, decor_css, photos]
        return(res)
    if request.method == 'PUT':
        album=Album.query.filter_by(id=aid).first()
        name=request.json['name']
        user_id=request.json['user_id']
        decor_css = request.json['decor_css']
        album.name = name
        album.user_id = user_id
        album.decor_css = decor_css
        db.session.add(album)
        db.session.commit()
        return {"message": "Album created succesfully"}
    if request.method == "DELETE":
        album=Album.query.filter_by(id=aid).first()
        db.session.delete(album)
        db.session.commit()
@app.route("/photos")
def photos():
    #Добавить проверку методов GET, POST, UPDATE, DELETE
    #Никита
    res = {"photos": []}
    photoslist = db.session.query(Photo).all();
    if request.method=="GET":
        for photo in photoslist:
            res["photos"].append(photo.json)
        return res
    #поменять data на json по образцу в users
    if request.method == 'POST':
        user_id=request.data['user_id']
        album_id=request.data['album_id']
        name = request.data['name']
        photo = request.data['photo']
        path = request.data['path']
        return photo

@app.route("/photos/<pid>")
def photo_page(pid):
    #Никита
    pass




app.run()
