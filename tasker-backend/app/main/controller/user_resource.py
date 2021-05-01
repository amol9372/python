import datetime
from http import HTTPStatus
from flask_restx import Resource, api
from app.main.db_models.user.user_pool import UserPool
from app.main.db_models.user.users import User
from app.main.aws_util import google_app_credentials
import jwt
from flask_jwt import jwt_required, current_identity
import json
from flask.globals import request
from app.main.util import UserDto
from app.main import transaction
from flask import jsonify, make_response, request, Response
from google_token import validate_id_token

api = UserDto.api


@api.route("register")
class RegisterUser(Resource):

    @transaction()
    def post(self):
        data = json.loads(request.data.decode())
        user_in_pool = UserPool(**data)
        # Check if user already exists or not
        if User.get_user(user_in_pool.email):
            return {"status": 200, "message": "User already exists"}

        print(user_in_pool)
        # Save user in UserPool and Users
        UserPool.register_user_in_pool(user_in_pool)
        user = User(user_in_pool.name, user_in_pool.email)
        User.create_user(user)
        return {"status": 201, "message": "User created in Pool", "user": user.name}


@api.route("login")
class LoginUser(Resource):

    def post(self):
        data = json.loads(request.data.decode())
        # check if user exits and password is correct
        user_from_pool: UserPool = UserPool.get_user_from_pool(data['email'])

        if user_from_pool and UserPool.check_password(password=data['password'], password_hash=user_from_pool.password):
            # Create JWT token and return it
 
            user : User = User.get_user(email=data["email"])
            
            # Save data in user context
 
            access_token = jwt.encode({
                'public_id': user.email,
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 'my_precious_secret_key')

            refresh_token = jwt.encode({
                'public_id': user.email,
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, 'my_secret_key')

            response: Response = make_response(jsonify({"token": access_token.decode(
                'UTF-8'), "refresh_token": refresh_token.decode("UTF-8"), "user": {"name": user.name, "email": user.email}}), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return {"status": 200, "message": "Invalid credentials, Please try again"}


@api.route("google-signin")
class GoogleLogin(Resource):

    @api.param(
        "id_token", "A JWT from the Google Sign-In SDK to be validated", _in="formData"
    )
    @api.response(HTTPStatus.FORBIDDEN, "Unauthorized")
    def post(self):
        # Validate the identity
        id_token = json.loads(request.data.decode())["id_token"]

        try:
            identity = validate_id_token(id_token, google_app_credentials["client_id"])
        except ValueError:
            return make_response(jsonify({"message": "Invalid ID token"}, HTTPStatus.FORBIDDEN))
        
        if not identity["email_verified"]:
            return make_response(jsonify({"message": "Email not verfied"}, HTTPStatus.FORBIDDEN))

        # save user to application if does not exists
        user_from_pool: UserPool = UserPool.get_user_from_pool(identity['email'])

        if not user_from_pool:
           UserPool.register_user_in_pool(UserPool(name=identity["name"], email=identity["email"],password=None, provider="Google"))
           user = User(identity["name"], identity["email"])
           User.create_user(user)

        # create access and refresh tokens
        access_token = jwt.encode({
                'public_id': user_from_pool.email,
                'name' : user_from_pool.name,
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 'my_precious_secret_key')
        
        refresh_token = jwt.encode({
                'public_id': user_from_pool.email,
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, 'my_secret_key')

        return make_response(jsonify({"access_token" : access_token.decode("UTF-8"), "refresh_token" : refresh_token.decode("UTF-8")}), 200)    

    def get(self):
        pass



@api.route("jwt-test")
class TestJwt(Resource):

    @jwt_required()
    def get(self):
        print(current_identity.__dict__)
        return {"status": 200, "message": "Able to access protected resource"}


response = {
  "iss": "accounts.google.com",
  "azp": "714233221839-k2tnu6te43b2flhh3na9dg64aqk556cs.apps.googleusercontent.com",
  "aud": "714233221839-k2tnu6te43b2flhh3na9dg64aqk556cs.apps.googleusercontent.com",
  "sub": "110870127022819412154",
  "email": "amolsingh9372@gmail.com",
  "email_verified": True,
  "at_hash": "umlyBGfYLmwajNn5bTYr-Q",
  "name": "amol singh",
  "picture": "https://lh3.googleusercontent.com/a-/AOh14GjaJaIAbIXq_ODs-c0T869VamUVFZ83jBY5o5OXIg=s96-c",
  "given_name": "amol",
  "family_name": "singh",
  "locale": "en-GB",
  "iat": 1619013743,
  "exp": 1619017343,
  "jti": "0f6adccccc8a4e95fac93f6d1157e2db9a37ddf7"
}
