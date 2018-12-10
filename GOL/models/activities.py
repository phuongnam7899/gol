from mongoengine import IntField,StringField,Document

class Activities(Document):
    tit = StringField()
    st = IntField()
    knl = IntField()
    cre = IntField()
    per = IntField()
    soc = IntField()
    