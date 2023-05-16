from flask import Flask, request, jsonify

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
    if request.method == "GET": #работает
        res = {"users": []}
        userslist = db.session.query(User).all()
        for user in userslist:
            res["users"].append(user.json)
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
        #добавить проверки на существование пользователя,
        if user != User.query.filter_by(user).first():
        #на совпадение с уже существующими логином и емэйл
            if mail!=User.query.filter_by(email),first():
                cur_user.login = login
                cur_user.mail = email
                cur_user.password = password
                db.session.add(cur_user)
                db.session.commit()
                return {"message": "User updated successfully"}
            else:
                return "данный адрес электронной почты уже зарегестрирован"
        else:
            return "такой пользователь уже есть"
            
    if request.method == "DELETE": #Никита - доработать
        # добавить проверки на существование пользователя
        if User.query.filter_by(name)==name:
            user = User.query.filter_by(id=uid).first()
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return "Такого пользователя нет"


@app.route("/albums", methods = ['post','get'])
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
def album_page(aid):
    if request.method == "GET":
        album=Album.query.filter_by(id=aid).first()
        if album:
            return album.json
        else:
            return{"error": "Album not found"}
        #Арсений - создать по образцу users - добавить проверки +

    if request.method == 'PUT': #Арсений - создать по образцу users - добавить проверки +
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
        '''
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
        #добавить проверки на существование пользователя,
        #на совпадение с уже существующими логином и емэйл
        cur_user.login = login
        cur_user.mail = email
        cur_user.password = password
        db.session.add(cur_user)
        db.session.commit()
        return {"message": "User updated successfully"}
        '''
    if request.method == "DELETE": #Арсений - создать по образцу users - добавить проверки +
        album=Album.query.filter_by(id=aid).first()
        if not album:
            return {"error": "no such album"}
        else:
            print('1')
            db.session.delete(album)
            print('2')
            db.session.commit() #не удаляется потому что есть фотографии связанаы с этим альбомом
            print('3')
            return {"message": "Album deleted succefully"}
        
@app.route("/photos", methods = ['post', ' get', 'delete', 'update'])
def photos(pid):
    #Добавить проверку методов GET, POST, UPDATE, DELETE
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
