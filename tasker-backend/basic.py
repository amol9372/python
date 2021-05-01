from logging import error
from flask import Flask, redirect, request
from flask.helpers import url_for
from flask.templating import render_template
from flask.wrappers import Response
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint, google
from requests.api import request
from flask_cors import CORS, cross_origin
import os

login_manager = LoginManager()

app = Flask(__name__) 
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:avizva9372@postgres-test-db.cqju9q6izhxh.ap-south-1.rds.amazonaws.com/python-test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
app.config['SECRET_KEY'] = "mysecretkey"
app.config['CORS_HEADERS'] = 'Content-Type'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_INSECURE_TOKEN_TRANSPORT'] = '1'

db = SQLAlchemy(app)

Migrate(app, db)

login_manager.init_app(app)

blueprint = make_google_blueprint(
    client_id="714233221839-k2tnu6te43b2flhh3na9dg64aqk556cs.apps.googleusercontent.com",
    client_secret=" ", offline=True, scope=["email"]
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/", methods=["GET"])
@cross_origin()
def home():
    # Response.headers.add("Access-Control-Allow-Origin", "*")
    if not google.authorized:
        print(url_for("google.login"))
        return redirect(url_for("google.login"))
    print(google.authorized)
    resp = google.get("/oauth2/v2/userinfo")  # userinfo endpoint
    print(resp.json())
    res = '<html><head><title>Main</title></head><body></body><script> window.opener.postMessage(resp.json(), "*");window.close();</script></html>'
    return res


# @cross_origin()
# @app.route("/login/google", methods=["GET"])
# def index():
#     # Enable Access-Control-Allow-Origin
#     # Response.headers.add("Access-Control-Allow-Origin", "*")
#     # return 'Amol Singh is the best'
#     if not google.authorized:
#         return render_template(url_for("google.login"))

#     print(google.authorized)
#     resp = google.get("/oauth2/v2/userinfo")  # userinfo endpoint
#     print("login/google" + resp)
#     return render_template("welcome.html", res=resp.json())


# @app.route("/login/google/authorized")
# def login():
#     code = request.args.get("code")
#     print("Auth Code is ::: {}".format(code))

@cross_origin()
@app.route("/home", methods=["GET"])
def index_2():
    # Enable Access-Control-Allow-Origin
    # Response.headers.add("Access-Control-Allow-Origin", "*")
    return 'Amol Singh is the best'


if __name__ == "__main__":
    context = ('E:\\certificates\\flask\\server.crt',
               'E:\\certificates\\flask\\server.key')  # certificate and key files
    app.run(ssl_context=context, debug=True)
    # app.run(debug=True)
