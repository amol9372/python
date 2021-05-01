from flask import json


class Test():

    def __init__(self, id, name):
        self.id = id
        self.name = name


t = Test(1, 'amol')

print(t)

print(json.dumps(t.__dict__))