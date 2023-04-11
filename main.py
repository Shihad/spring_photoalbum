from flask import Flask

from models import db, User, Album, Photo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you_cant_guess_this_key'

db.init_app(app)

#Дмитрий
@app.route("/users")
def users():
    pass

@app.route("/photos")
def photos():
    pass

@app.route("/albums")
def albums():
    pass
app.run()