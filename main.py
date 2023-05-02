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
        #на совпадение с уже существующими логином и емэйл
        cur_user.login = login
        cur_user.mail = email
        cur_user.password = password
        db.session.add(cur_user)
        db.session.commit()
        return {"message": "User updated successfully"}
    if request.method == "DELETE": #Никита - доработать
        # добавить проверки на существование пользователя
        user = User.query.filter_by(id=uid).first()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

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



@app.route("/albums/<aid>")
def album_page(aid):
    if request.method == "GET":
        album=Album.query.filter_by(id=aid).first()
        #Арсений - создать по образцу users - добавить проверки
        name=album.name
        user_id=album.user_id
        decor_css = album.decor_css
        photos=album.photos
        #return(name) <-- нормально выводит имя
        #заменить на словарь
        #res={"name":name, user_id, decor_css}
        res={}
        return(res)
    if request.method == 'PUT': #Арсений - создать по образцу users - добавить проверки
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
    if request.method == "DELETE": #Арсений - создать по образцу users - добавить проверки
        album=Album.query.filter_by(id=aid).first()
        db.session.delete(album)
        db.session.commit()
        
@app.route("/photos")
def photos():
    #Добавить проверку методов GET, POST, UPDATE, DELETE
    #Богдан
    res = {"photos": []}
    photoslist = db.session.query(Photo).all();
    if request.method=="GET":
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

@app.route("/photos/<pid>")
def photo_page(pid):
    #Никита
    if request.method == "GET":
        photo=Photo.query.filter_by(id=pid).first()
        #добавить проверки на существование фото
        return photo.json
    #добавить update и delete



app.run()
