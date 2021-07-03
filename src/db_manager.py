import json
from pathlib import Path
from exceptions import TypeDoesNotExist, TableDoesNotExist


class DBObject:
    types = None
    db_file = None

    def __init__(self, **db_file):
        self.db_file = db_file
        self.types = db_file.get("types", {})

    def create_type(self, type_name, *attrs, **kwargs):
        self.types.update(
            {type_name: {
                "pk_count": 0,
                "meta_data": {
                        "fields": attrs,
                        ** kwargs,
                    },
                    "records": {},
                }
            }
        )
        self.db_file["type_counter"] += 1

    def inherit_type(self, type_name, inherited, *attrs, **kwargs):
        _type = self.__get_type(inherited)
        fields = list(set(_type["meta_data"]["fields"].extend(attrs)))
        self.create_type(type_name, *fields, **kwargs)

    def delete_type(self, type_name, *args, **kwargs):
        del self.types.get(type_name, None)

    def list_type(self):
        return self.types

    def __get_type(self, type_name):
        _type = self.types.get(type_name, None)
        if _type is None:
            raise TableDoesNotExist(f'Type name "{type_name}" does not in the pages.')
        return _type

    def create_recored(self, type_name, primary_key=None, **fields):
        _type = self.__get_type(type_name)
        if primary_key is None:
            primary_key = _type["pk_count"] + 1
            _type["pk_count"] += 1
        _fields = _type['meta_data']['fields']
        _type['records'].update({
            primary_key: {
                **dict(zip(_fields, fields))
            }
        })

    def update_recored(self, type_name, primary_key, **fields):
        self.create_recored(type_name, primary_key=primary_key, **fields)

    def delete_recored(self, type_name, primary_key):
        _type = self.__get_type(type_name)
        del _type['records'][primary_key]

    def search_recored(self, type_name, primary_key):
        _type = self.__get_type(type_name)
        return _type['records'].get(primary_key, None)
    
    def list_recoreds(self, type_name):
        _type = self.__get_type(type_name)
        return _type.get('records')

    def filter_recoreds(self, type_name, field, operator, value):
        _type = self.__get_type(type_name)
        records = _type.get('records')
        valid_data = {}
        for recored in records:
            if eval(f"{records[recored]['fields']}{operator}{value}"):
                valid_data.update({recored:{**records[records]}})
        return valid_data

    def commit(self):
        json.dump(self.db_file)


class HaloDB:
    def __init__(self, filename=None):
        if filename:
            fn = filename.split()[:-1]
            self.create_connection(filename=f"{fn}.json")

    def create_connection(self, filename):
        try:
            with open(filename, "r") as f:
                json_data = json.load(f)
        except FileNotFoundError:
            with open(filename, "w") as f:
                json.dump({"type_counter": 0, "types": {}}, f)
