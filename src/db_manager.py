import json
<<<<<<< HEAD
from pathlib import Path
from exceptions import TypeDoesNotExist, TableDoesNotExist
=======

from exceptions import TypeDoesNotExist, TypeAlreadyExist, DuplicatedPrimaryKey, UniqueConstraintError
>>>>>>> 5de67cc3e32b2453b6ae9495b2aee8ee5e9012af


class DBObject:
    types = None
    db_file = None

    def __init__(self, filename, **db_file):
        self.db_file = db_file
        self.filename = filename
        self.types = db_file.get("types", {})

    def __compare(self, val1, val2, operator):
        if isinstance(val1, str) and isinstance(val2, str):
            return eval(f'"{val1}" {operator} "{val2}"')
        if isinstance(val1, int) and isinstance(val2, int):
            return eval(f'{val1} {operator} {val2}')
        raise TypeError("cannot compare different data types.")


    def create_type(self, type_name, *attrs, **kwargs):
        if self.types.get(type_name) is not None:
            raise TypeAlreadyExist(f"Type {type_name} already exist in the file.")
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
        _type = self.types.get(type_name, None)
        if _type is not None:
            del self.types[type_name]

    def list_type(self):
        return self.types

    def __get_type(self, type_name):
        _type = self.types.get(type_name, None)
        if _type is None:
            raise TableDoesNotExist(f'Type name "{type_name}" does not in the pages.')
        return _type

    def create_recored(self, type_name, *fields, **kwargs):
        _type = self.__get_type(type_name)
        primary_key = kwargs.get('primary_key')
        if _type['records'].get(primary_key, None) is not None:
            raise DuplicatedPrimaryKey()
        if primary_key is None:
            primary_key = _type["pk_count"] + 1
            _type["pk_count"] += 1
        _fields = _type['meta_data']['fields']
<<<<<<< HEAD
=======
        unique_field = _type["meta_data"].get('unique', None)
        data = dict(zip(_fields, fields))
        if unique_field is not None:
            for field in unique_field:
                if self.filter_recoreds(type_name, field, data.get(field), '='):
                    raise UniqueConstraintError(f"Duplcated {field}.")
>>>>>>> 5de67cc3e32b2453b6ae9495b2aee8ee5e9012af
        _type['records'].update({
            int(primary_key): {
                **data
            }
        })
        return {'primary_key': primary_key, **dict(zip(_fields, fields))}

    def update_recored(self, type_name, primary_key, **fields):
        self.create_recored(type_name, primary_key=primary_key, **fields)

    def delete_recored(self, type_name, primary_key):
        _type = self.__get_type(type_name)
        if _type['records'].get(primary_key, None) is not None:
            del _type['records'][primary_key]

    def search_recored(self, type_name, primary_key):
        _type = self.__get_type(type_name)
        return _type['records'].get(primary_key, None)
    
    def list_recoreds(self, type_name):
        _type = self.__get_type(type_name)
        return _type.get('records')

    def filter_recoreds(self, type_name, field, value, operator):
        _type = self.__get_type(type_name)
        recordes = _type.get('records')
        valid_data = {}
<<<<<<< HEAD
        for recored in records:
            if eval(f"{records[recored]['fields']}{operator}{value}"):
                valid_data.update({recored:{**records[records]}})
=======
        operator = '==' if operator == '=' else operator
        field = int(field) if field.isdigit() else str(field)
        value = int(value) if value.isdigit() else str(value)
        for recored in recordes:
            if self.__compare(recordes[recored][field], value, operator):
                valid_data.update({recored:{**recordes[recored]}})
        if len(valid_data) == 1:
            primary_key = list(valid_data.keys())[0]
            valid_data = {'primary_key': int(primary_key), **valid_data[primary_key]}
>>>>>>> 5de67cc3e32b2453b6ae9495b2aee8ee5e9012af
        return valid_data

    def commit(self):
        with open(self.filename, "w") as f:
            json.dump(self.db_file, f)


class HaloDB:

    def get_connection(self, filename):
        filename = f"{filename}.json"
        try:
            with open(filename, "r") as f:
                json_data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open(filename, "w") as f:
                json_data = {"type_counter": 0, "types": {}}
                json.dump(json_data, f)
        return DBObject(filename, **json_data)


halo_db = HaloDB()
db = halo_db.get_connection("halodb")
try:
    db.create_type("users", "username", "password", unique=("username",))
    db.commit()
except TypeAlreadyExist:
    pass