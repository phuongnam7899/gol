from mongoengine import *

class Friend(Document):
    username = StringField()
    friend = ListField()
    password = StringField()
    avt = StringField()

