from mongoengine import IntField,StringField,Document

class All_history(Document):
    user = StringField()
    tit = StringField()
    des = StringField()
    img = StringField()
    time = StringField()
    st = IntField()
    knl = IntField()
    cre = IntField()
    per = IntField()
    soc = IntField()
    