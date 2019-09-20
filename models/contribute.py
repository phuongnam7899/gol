from mongoengine import *

class Contribute(Document):
    user = StringField()
    tit = StringField()
    st = IntField()
    per = IntField()
    knl = IntField()
    soc = IntField()
    cre = IntField()
     