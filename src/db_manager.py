import json
import os
from pathlib import Path

from .exceptions import (
    DuplicatedPrimaryKey,
    TypeAlreadyExist,
    TypeDoesNotExist,
    UniqueConstraintError,
    FileLimitExceded,
)


class DBObject:
    types = None
    db_file = None

    def __init__(self, filename, **db_file):
        all_db_data = {
            "type_counter": 0,
            "types": {}
        }
        previous = filename
        while previous is not None:
            with open(previous, 'r') as file:
                json_data = json.load(file)
                previous = json_data.get('prev', None)
                _types = json_data.get('types')
                for key in _types.keys():
                    if all_db_data['types'].get(key, None) is None:
                        all_db_data['types'][key] = {"pk_count":0, 'records': {}}
                all_db_data['type_counter'] += len(all_db_data['types'])
                for key in _types:
                    all_db_data['types'][key]['meta_data'] = _types[key]['meta_data']
                    all_db_data['types'][key]['meta_data']
                    all_db_data['types'][key]['pk_count'] += _types[key]['pk_count']
                    all_db_data['types'][key]['records'].update(_types[key]['records'])

        self.all_db_data = all_db_data
        self.db_file = db_file
        self.filename = filename
        self.types = self.all_db_data.get("types", {})

    def __compare(self, val1, val2, operator):
        val1 = int(val1) if val1.isdigit() else str(val1)
        if isinstance(val1, str) and isinstance(val2, str):
            return eval(f'"{val1}" {operator} "{val2}"')
        if isinstance(val1, int) and isinstance(val2, int):
            return eval(f"{val1} {operator} {val2}")
        raise TypeError("cannot compare different data types.")

    def create_type(self, type_name, *attrs, **kwargs):
        if self.types.get(type_name) is not None:
            raise TypeAlreadyExist(f"Type {type_name} already exist in the file.")
        data = {
                type_name: {
                    "pk_count": 0,
                    "meta_data": {
                        "fields": attrs,
                        **kwargs,
                    },
                    "records": {},
                }
            }
        self.db_file['types'].update(data)
        self.db_file['type_counter'] += 1
        self.types.update(data)
        self.all_db_data["type_counter"] += 1
        self.all_db_data['types'].update(data)

    def inherit_type(self, type_name, type_target, *attrs, **kwargs):
        _type = self.__get_type(type_target)
        fields = _type['meta_data']['fields']
        fields += attrs
        meta_data = _type['meta_data'].copy()
        meta_data.update(**kwargs)
        self.create_type(type_name, *fields[0], **meta_data)

    def delete_type(self, type_name, *args, **kwargs):
        filename = self.filename
        previous_deleted = False
        while filename is not None:
            with open(filename, 'r') as file:
                json_data = json.load(file)
                if previous_deleted:
                    json_data['next'] = None
                    previous_deleted = False
                _type = json_data['types'].get(type_name, None)
                if _type is not None:
                    del json_data['types'][type_name]
                    json_data['type_counter'] -= 1
            if json_data['type_counter'] < 1 and json_data['prev'] is not None:
                os.remove(filename)
                previous_deleted = True
            else:
                with open(filename, 'w') as file:
                    json.dump(json_data, file)
            filename = json_data.get('prev')

    def list_type(self):
        return self.types

    def __get_type(self, type_name):
        _type = self.types.get(type_name, None)
        if _type is None:
            raise TypeDoesNotExist(f'Type name "{type_name}" does not in the pages.')
        return _type

    def create_recored(self, type_name, *fields, **kwargs):
        _type = self.__get_type(type_name)
        primary_key = kwargs.get("primary_key")
        if _type["records"].get(primary_key, None) is not None:
            raise DuplicatedPrimaryKey()
        if primary_key is None:
            primary_key = _type["pk_count"] + 1
        _fields = _type["meta_data"]["fields"]
        unique_field = _type["meta_data"].get("unique", None)
        data = dict(zip(_fields, fields))
        if unique_field is not None:
            for field in unique_field:
                if self.filter_recoreds(type_name, field, data.get(field), "="):
                    raise UniqueConstraintError(f"Duplcated {field}.")
        _type["records"].update({int(primary_key): {**data}})
        _type["pk_count"] += 1
        if self.db_file['types'].get(type_name, None) is None:
            self.db_file['types'][type_name] = {'records': {}}
            self.db_file['types'][type_name]['meta_data'] = _type['meta_data']
        self.db_file['types'][type_name]['records'].update({int(primary_key): data})
        self.db_file['types'][type_name]['pk_count'] = _type['pk_count']
        self.db_file['type_counter'] = len(self.db_file['types'])
        return {"primary_key": int(primary_key), **data}

    def update_recored(self, type_name, primary_key, *fields):
        filename = self.filename
        is_available = False
        while filename is not None:
            with open(filename, 'r') as file:
                json_data = json.load(file)
                if json_data['types'][type_name]['records'].get(primary_key, None) is not None:
                    _fields = json_data['types'][type_name]['meta_data']['fields']
                    data = dict(zip(_fields, fields))
                    json_data['types'][type_name]['records'][int(primary_key)] = data
                    self.all_db_data['types'][type_name]['records'][int(primary_key)] = data
                    is_available = {'primary_key': int(primary_key), **data}
            if is_available:
                with open(filename, 'w') as file:
                        json.dump(json_data, file)
                return is_available
            filename = json_data.get('prev')
        return None

    def delete_recored(self, type_name, primary_key):
        filename = self.filename
        found = False
        while filename is not None:
            with open(filename, 'r') as file:
                json_data = json.load(file)
                if json_data['types'][type_name]['records'].get(primary_key, None) is not None:
                    del json_data['types'][type_name]['records'][int(primary_key)]
                    del self.all_db_data['types'][type_name]['records'][int(primary_key)]
                    found = True
            if found:
                with open(filename, 'w') as file:
                    json.dump(json_data, file)
                return found
            filename = json_data.get('prev')
        return found

        _type = self.__get_type(type_name)
        if _type["records"].get(primary_key, None) is not None:
            del _type["records"][int(primary_key)]

    def search_recored(self, type_name, primary_key):
        _type = self.__get_type(type_name)
        return _type["records"].get(int(primary_key), None)

    def list_recoreds(self, type_name):
        _type = self.__get_type(type_name)
        return _type.get("records")

    def filter_recoreds(self, type_name, field, value, operator):
        _type = self.__get_type(type_name)
        recordes = _type.get("records")
        valid_data = {}
        operator = "==" if operator == "=" else operator
        value = int(value) if value.isdigit() else str(value)
        for recored in recordes:
            if self.__compare(recordes[recored][field], value, operator):
                valid_data.update({recored: {**recordes[recored]}})
        if len(valid_data) == 1:
            primary_key = list(valid_data.keys())[0]
            valid_data = {"primary_key": int(primary_key), **valid_data[int(primary_key)]}
        return valid_data

    def commit(self):
        with open(self.filename, "w") as f:
            json.dump(self.db_file, f)


class HaloDB:
    def get_connection(self, filename):
        try:
            ufilename = self.__next_free_file(f"src/db/{filename}.json")
            previous = None
            file_size = Path(ufilename).stat().st_size
            json_data = None
            if file_size > 32 * 10:
                new_filename = f"src/db/{filename}_{os.urandom(2).hex()}.json"
                with open(ufilename, "r") as f:
                    json_data = json.load(f)
                with open(ufilename, 'w') as f:
                    json_data['next'] = new_filename
                    json.dump(json_data, f)
                    previous = ufilename
                ufilename = new_filename
                raise FileLimitExceded("")
            with open(ufilename, "r") as f:
                json_data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError, FileLimitExceded):
            with open(ufilename, "w") as f:
                json_data = {"type_counter": 0, "prev": previous, "next": None, "types": {}}
                json.dump(json_data, f)
        return DBObject(ufilename, **json_data)

    def __next_free_file(self, filename):
        try:
            with open(filename, "r") as f:
                json_data = json.load(f)
                while json_data['next'] is not None:
                    with open(json_data['next'], 'r') as file:
                        filename = file.name
                        json_data = json.load(file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        return filename

halo_db = HaloDB()
db = halo_db.get_connection("halodb")
try:
    if db.all_db_data['types'].get('users', None) is None:
        db.create_type("users", "username", "password", unique=("username",))
        db.commit()
except TypeAlreadyExist:
    pass
