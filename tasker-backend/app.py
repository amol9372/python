from http import HTTPStatus
import json
from flask.views import http_method_funcs
from flask_cors.core import ACL_CREDENTIALS
from flask_login import current_user
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import Flask, request


# from flask_restx import Api, Resource, fields
from flask_restx import Api, Resource, fields
from werkzeug.utils import header_property
from app.main.models.model_google import user_manager, user_google
from google_token import validate_id_token
from app.main.aws_util import google_app_credentials
from flask_cors import CORS
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

try:
    app.config["GOOGLE_CLIENT_ID"] = google_app_credentials["client_id"]
    app.secret_key = "my secret key is good"
    # app.config['REMEMBER_COOKIE_HTTPONLY'] = True
except RuntimeError:

    pass

login = LoginManager()
login.init_app(app)

api = Api(
    app=app, title="Google Sign in App", description="Demonstrate Sigin with Google"
)

# app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


user_manager = user_manager.UserManager()


# load user from application
@login.user_loader
def user_loader(user_id):
    user = user_manager.lookup_user(user_id)
    return user


# Add this decorator to all mutating operations.
def csrf_protection(fn):
    """Require that the X-Requested-With header is present."""

    def protected(*args):
        if "X-Requested-With" in request.headers:
            return fn(*args)
        else:
            return "X-Requested-With header missing", HTTPStatus.FORBIDDEN

    return protected


a_user = api.model(
    "User",
    {
        "google_id": fields.Integer(description="The user's Google account ID"),
        "name": fields.String(description="The user's full name"),
        "picture": fields.Url(description="A URL to the profile image"),
    },
)


@api.route("/me")
class Me(Resource):
    @login_required
    @csrf_protection
    @api.response(HTTPStatus.OK, "Success", a_user)
    def get(self):
        return {
            "google_id": current_user.id,
            "name": current_user.name,
            "picture": current_user.profile_pic,
        }

    @csrf_protection
    @api.param(
        "id_token", "A JWT from the Google Sign-In SDK to be validated", _in="formData"
    )
    @api.response(HTTPStatus.OK, "Success", a_user)
    @api.response(HTTPStatus.FORBIDDEN, "Unauthorized")
    def post(self):

        # Validate the identity
        id_token = json.loads(request.data.decode())["id_token"]
        if id_token is None:
            return "No ID token provided", HTTPStatus.FORBIDDEN

        try:
            identity = validate_id_token(id_token, app.config["GOOGLE_CLIENT_ID"])
        except ValueError:
            return "Invalid ID token", HTTPStatus.FORBIDDEN

        # Get the user info out of the validated identity
        if "sub" not in identity or "name" not in identity or "picture" not in identity:
            return "Unexcpected authorization response", HTTPStatus.FORBIDDEN

        # This just adds a new user that hasn't been seen before and assumes it
        # will work, but you could extend the logic to do something different
        # (such as only allow known users, or somehow mark a user as new so
        # your frontend can collect extra profile information).
        user = user_manager.add_or_update_google_user(
            identity["sub"], identity["name"], identity["picture"]
        )

        # Authorize the user:
        user_log_in = login_user(user, force=True)

        return self.get()

    @login_required
    @csrf_protection
    @api.response(HTTPStatus.NO_CONTENT, "Success")
    def delete(self):
        print(current_user.is_authenticated)
        logout_user()
        return {"status": "user logged out successfully"}, HTTPStatus.NO_CONTENT


@api.route("/sample")
class Sample(Resource):
    def get(self):
        return {"status": "success"}, HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
