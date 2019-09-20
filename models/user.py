from mongoengine import *

class User(Document):
    fullname = StringField() 
    username = StringField()
    email = StringField()
    password = StringField()
    birthday = StringField()
    gender = StringField() 
    phone = StringField()
    avt = StringField(default = "https://cdn1.iconfinder.com/data/icons/ninja-things-1/1772/ninja-simple-512.png") 