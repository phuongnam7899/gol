from mongoengine import *

class Attribute(Document):
    username = StringField()
    st = IntField(default = 0)
    knl = IntField(default = 0)
    cre = IntField(default = 0)
    per = IntField(default = 0)
    soc = IntField(default = 0)