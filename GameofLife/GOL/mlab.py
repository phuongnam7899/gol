import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds125841.mlab.com:25841/gameoflife

host = "ds125841.mlab.com"
port = 25841
db_name = "gameoflife"
user_name = "admin"
password = "admin1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())