from mongoengine import *

class User(Document):
    fullname = StringField() 
    username = StringField()
    email = StringField()
    password = StringField()
    birthday = StringField()
    gender = StringField() 
    phone = StringField() 