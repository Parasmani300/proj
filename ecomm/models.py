from ecomm import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class User(db.Document,UserMixin):
    user_id = db.StringField(unique=True)
    firstname = db.StringField(max_length=50)
    lastname = db.StringField(max_length=50)
    password = db.StringField(max_length=255)
    phone_no = db.StringField(max_length=20)
    email = db.StringField(unique=True,max_length=30)

    def set_password(self,password):
        self.password = generate_password_hash(password)
    
    def get_password(self,password):
        return check_password_hash(self.password,password)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

class Products(db.Document):
    _id = db.ObjectIdField()
    id = db.StringField(unique=True)
    name= db.StringField(max_length=50)
    description = db.StringField(max_length=255)
    price = db.StringField(max_length=5)
    trending = db.BooleanField(default=False)