
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
app = Flask(__name__)

app.config.from_object(Config)


from ecomm import routes


if __name__ == "__main__":
    app.run()
