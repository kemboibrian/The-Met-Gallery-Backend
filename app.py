

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from model import db, User  
import bcrypt
from auth import admin_required
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

class Signup(Resource):
    def post(self):
        args = request.get_json()
        if not all(k in args for k in ('username', 'email', 'password', 'role')):
            return {'message': 'Username, email, password, and role are required'}, 400
        
        hashed_password = bcrypt.hashpw(args['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=args['username'], email=args['email'], password=hashed_password, role=args['role'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': f"{args['role'].capitalize()} created successfully"}, 201
    

class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        self.parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

    def post(self):
        args = self.parser.parse_args()
        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': f"{user.role.capitalize()} logged in successfully", 'access_token': access_token})
        
        return jsonify({'message': 'Invalid email or password'}), 401

class Logout(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return {'message': f"{user.role.capitalize()} logged out successfully"}, 200

if __name__ == '__main__':
    app.run(debug=True)