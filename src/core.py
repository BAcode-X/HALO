import json
import csv
import uuid

class Record:
    
    planet = "E226 - S187"
    primary_key = None

    def __init__(self):
        primary_key = uuid.uuid4()

    def create(self, *args):
        
        pass

    def delete(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def list_all(self, *args, **kwargs):
        pass

    def _filter(self, *args, **kwargs):
        pass