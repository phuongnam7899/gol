from mongoengine import *

class Attribute(Document):
    username = StringField()
    st = IntField(default = 1)
    knl = IntField(default = 1)
    cre = IntField(default = 1)
    per = IntField(default = 1)
    soc = IntField(default = 1)