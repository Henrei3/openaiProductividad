from Model.recordingsDB import Simple, SimpleSchemaPost
import requests


def make_post_simple():
    url = "http://127.0.0.1:5000/simple"

    simple_post_object = Simple(10)

    to_json = SimpleSchemaPost().dump(simple_post_object)

    x = requests.post(url, json=to_json)

    print(x.text)


make_post_simple()
