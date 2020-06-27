
from flask import Flask
from config import Config
import pyrebase

app = Flask(__name__)

app.config.from_object(Config)
firebaseConfig = {
    'apiKey': "AIzaSyBLY55vpRB8OzjXYrGb4v9i3RBtHP58Nn8",
    'authDomain': "bearit-d00aa.firebaseapp.com",
    'databaseURL': "https://bearit-d00aa.firebaseio.com",
    'projectId': "bearit-d00aa",
    'storageBucket': "bearit-d00aa.appspot.com",
    'messagingSenderId': "74649264653",
    'appId': "1:74649264653:web:8da9a8c99b1cd8ad3b2b44",
    'measurementId': "G-00LF9J63Z8"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

db = firebase.database()

from ecomm import routes


if __name__ == "__main__":
    app.run()
