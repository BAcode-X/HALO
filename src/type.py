import json
import uuid


class Type:

    planet = "E226 - S187"
    primary_key = None
    
    def __init__(self):
        self.primary_key = uuid.uuid4()

    def create(self, number, *args):
        pass

    def delete(self, *args, **kwargs):
        pass

    def inherit(self, *args, **kwargs):
        pass

    def list_all(self, *args, **kwargs):
        pass