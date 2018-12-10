from mongoengine import *

class Information(Document):
    username = StringField()
    email = StringField()
    fullname = StringField()
    password = StringField()