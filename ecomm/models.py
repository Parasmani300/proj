from ecomm import db

class User(db.Document):
    user_id = db.IntField(unique=True)
    firstname = db.StringField(max_length=50)
    lastname = db.StringField(max_length=50)
    password = db.StringField(max_length=255)
    phone_no = db.StringField(max_length=20)
    email = db.StringField(max_length=30)

class Products(db.Document):
    _id = db.ObjectIdField()
    id = db.StringField(unique=True)
    name= db.StringField(max_length=50)
    description = db.StringField(max_length=255)
    price = db.StringField(max_length=5)
    trending = db.BooleanField(default=False)