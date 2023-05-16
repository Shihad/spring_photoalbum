from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models import db, User, Album, Photo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you_cant_guess_this_key'
app.config['CORS_HEADERS'] = 'Content-Type'
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
    album2 = Album('Свадьба Ивановых', user1.id)
    db.session.add(album2)
    db.session.commit()
    photo1 = Photo(user1.id, album2.id, "static/img/1.jpg","Мы с Серегой")
    photo2 = Photo(user1.id, album1.id, "static/img/2.jpg", "Ялта")
    photo3 = Photo(user1.id, album1.id, "static/img/3.jpg", "Сочи")
    db.session.add(photo1)
    db.session.add(photo2)
    db.session.add(photo3)
    db.session.commit()

# Дмитрий
@app.route("/users", methods = ['post','get'])
def users():
    if request.method == "GET": #работает
        res = {"users": []}
        userslist = db.session.query(User).all()
        for user in userslist:
            res["users"].append(user.json)
        # В userlist добавить разделы albums - передать JSON альбомов
        # и раздел preview - по одной фотографии от каждого фотоальбома
        # Арсений
        return res
    if request.method == "POST": #работает
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

@app.route("/users/<uid>", methods = ['put','get', 'delete'])
def user_page(uid):
    if request.method == "GET": #работает
        user = User.query.filter_by(id=uid).first()
        if user:
            return user.json
        else:
            return {"error":"User not found"}
    if request.method == "PUT": #работает
        cur_user = User.query.filter_by(id=uid).first()
        login = request.json['login']
        password = request.json['password']
        email = request.json['email']
        user = User.query.filter_by(login=login).first()
        if user and user!=cur_user:
            return {"error": "This login already registered"}
        user = User.query.filter_by(mail=email).first()
        if user and user!=cur_user:
            return {"error": "This email already registered"}
        if not cur_user:
            return {"error": "No such user"}
        cur_user.login = login
        cur_user.mail = email
        cur_user.password = password
        db.session.add(cur_user)
        db.session.commit()
        return {"message": "User updated successfully"}

            
    if request.method == "DELETE": #Никита - доработать
        # добавить проверки на существование пользователя
        user = User.query.filter_by(id=uid).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return {'error':"Такого пользователя нет"}


@app.route("/albums", methods = ['post','get'])
@cross_origin()
def albums():
    # Добавить проверку методов GET, POST, UPDATE, DELETE
    if request.method == "GET": #работает
        res = {"albums": []}
        albumslist = db.session.query(Album).all()
        for album in albumslist:
            res["albums"].append(album.json)
        return res
    if request.method == "POST": #Никита
        name = request.json['name']
        user_id = request.json['']
        album = Album(name, user_id)
        db.session.add(album)
        db.session.commit()



@app.route("/albums/<aid>", methods = ['post','get', 'PUT', "DELETE"])
@cross_origin()
def album_page(aid):
    if request.method == "GET":
        album=Album.query.filter_by(id=aid).first()
        dict = album.json
        dict['photos'] = []
        #разобраться, почему не работает album.photos
        #Дмитрий
        alb_photos = Photo.query.filter_by(album_id=album.id).all()
        print(alb_photos)
        for photo in alb_photos:
            dict['photos'].append(photo.json)
        if album:
            return dict
        else:
            return{"error": "Album not found"}

    if request.method == 'PUT':
        cur_album=Album.query.filter_by(id=aid).first()
        name=request.json['name']
        user_id=request.json['user_id']
        decor_css = request.json['decor_css']
        album=Album.query.filter_by(user_id=user_id).first()
        if not album:
            return {"error":"no such album"}
        cur_album.name = name
        cur_album.user_id = user_id
        cur_album.decor_css = decor_css
        db.session.add(cur_album)
        db.session.commit()
        return {"message": "Album updated succesfully"}

    if request.method == "DELETE":
        album=Album.query.filter_by(id=aid).first()
        if not album:
            return {"error": "no such album"}
        else:
            db.session.delete(album)
            db.session.commit()
            return {"message": "Album deleted succefully"}
        
@app.route("/photos", methods = ['post', 'get', 'delete', 'put'])
def photos():
    #Добавить проверку методов GET, POST, PUT, DELETE
    #Богдан
    if request.method=="GET":
        res = {"photos": []}
        photoslist = db.session.query(Photo).all()
        for photo in photoslist:
            res["photos"].append(photo.json)
        return res
    if request.method == 'POST':
        user_id=request.json['user_id']
        album_id=request.json['album_id']
        shot_date = request.json['shot_date']
        comment = request.json['comment']
        path = request.json['path']
        photo = Photo(user_id, album_id, path,comment,shot_date)
        db.session.add(photo)
        db.session.commit()
    #метод PUT
    #Богдан
    if request.method == "DELETE":
        photo=Photo.query.filter_by(id=pid).first()
        if photo:
            db.session.delete(photo)
            db.session.commit()
        else:
            return {'message': 'no such photo'}



@app.route("/photos/<pid>")
def photo_page(pid):
    #Никита
    if request.method == "GET":
        photo=Photo.query.filter_by(id=pid).first()
        #добавить проверки на существование фото
        return photo.json
    #добавить update и delete



app.run()
