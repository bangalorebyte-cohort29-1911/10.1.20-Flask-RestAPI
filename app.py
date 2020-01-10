from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/')
def index():
    return "Welcome to User REST API"

@app.route('/user', methods = ['GET','POST','PUT',"DELETE"])
def user():
    if request.method == 'GET':
        all_users = User.query.all()
        all_users_json = users_schema.dump(all_users)
        return f'GET data:{all_users_json}'
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return f'POST User:{name} created'
    elif request.method == 'PUT':
        check_id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        check_user = User.query.get(check_id)
        check_user.name = name
        check_user.email = email
        db.session.commit()
        return f'PUT : Updated User:{name}'
    elif request.method == 'DELETE':
        check_id = request.form['id']
        check_user = User.query.get(check_id)
        db.session.delete(check_user)
        db.session.commit()
        return f'DELETE User:{check_user.name} is deleted'
    else:
        return 'METHOD Not Defined for User'

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)









