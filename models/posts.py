from mongoengine import Document,StringField, IntField, ListField
import mlab

mlab.connect()

class Post(Document):
    tit = StringField()
    descript = StringField()
    img = StringField()
    user = StringField()
    like = IntField(default=0)
    wholike = ListField()
    comments = ListField()


#Post(tit="abcd",descript='ádds',img = "https://previews.123rf.com/images/artshock/artshock1209/artshock120900045/15221647-imag-of-heart-in-the-blue-sky-against-a-background-of-white-clouds-.jpg",user="phuongnam7899").save()
