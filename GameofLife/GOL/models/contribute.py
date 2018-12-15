from mongoengine import *

class Contribute(Document):
    tit = StringField()
    st = IntField()
    per = IntField()
    knl = IntField()
    soc = IntField()
    cre = IntField()
     