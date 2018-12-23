from mongoengine import Document,IntField,StringField

class Habit(Document):
    username = StringField()
    tit = StringField()
    streak = IntField(default = 0)
    st = IntField()
    knl = IntField()
    cre = IntField()
    per = IntField()
    soc = IntField()