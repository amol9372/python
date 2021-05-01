import os
from flask_jwt import JWT
from app.main.jwt_utils.jwt_handlers import authenticate, identity
from app import blueprint
from app.main import create_app
from app.main.aws_util import google_app_credentials
from flask_cors import CORS

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.app_context().push()

JWT(app, authenticate, identity)

app.register_blueprint(blueprint)

app.config["GOOGLE_CLIENT_ID"] = google_app_credentials["client_id"]

cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

if __name__ == "__main__":
    app.run()
