import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds127634.mlab.com:27634/gol

host = "ds127634.mlab.com"
port = 27634
db_name = "gol"
user_name = "nam"
password = "admin1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())