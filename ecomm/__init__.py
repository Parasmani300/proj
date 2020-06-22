
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from itsdangerous import URLSafeTimedSerializer
app = Flask(__name__)

app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
#login_serializer = URLSafeTimedSerializer(app.secret_key)
from ecomm import routes


if __name__ == "__main__":
    app.run()
