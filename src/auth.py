import json
import os
import uuid
from hashlib import pbkdf2_hmac

from exceptions import InvalidCreaditioal, ForbidenAccess, MultipleValueReturned

from db_manager import db

class User:
    planet = "E226-S187"
    primary_key = None
    username = None
    USERNAME, PASSWORD, PRIMARY_KEY = "username", "password", "primary_key"
    __fields = [PRIMARY_KEY, USERNAME, PASSWORD]

    def __init__(self, primary_key, username):
        self.primary_key = primary_key
        self.username = username

    def __setattr__(self, attr, value, *args, **kwargs):
        if getattr(self, attr, None) is not None and attr == self.PRIMARY_KEY:
            raise ForbidenAccess('cannot set a primary key.')
        if attr not in self.__fields:
            raise ForbidenAccess(f"Setting an attribute '{attr}'' is forbiden.")
        return super().__setattr__(attr, value, *args, **kwargs)

    def __repr__(self):
        return f"<User '{self.username}'>"


class UserManager:
    @classmethod
    def create_user(cls, username, password, new_password):
        if password != new_password:
            raise InvalidCreaditioal("Password mismatched")
        if not username.isalnum():
            raise TypeError("Username must be alphanumeric.")
        hashed_password = cls.__hash_password(password)
        user_data = cls.__create_user(username, hashed_password)
        user = User(None, None)
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    @classmethod
    def __create_user(cls, username, hashed_password):
        user = db.create_recored("users", username, hashed_password)
        db.commit();
        return user


    @classmethod
    def __get_all_users(cls):
        json_data = {}
        with open("users.json", "r") as f:
            try:
                json_data = json.load(f)["data"]
            except json.decoder.JSONDecodeError:
                json.dump(json_data, f)
        return json_data

    @classmethod
    def __hash_password(cls, password):
        hashed_password = pbkdf2_hmac(
            "sha256", f"{password}".encode(), b"3cd83f359b2e8db6a3b0", 100000
        )
        return hashed_password.hex()

    @classmethod
    def authenticate(cls, username, password):
        user_data = db.filter_recoreds('users', 'username', '=', username)
        if len(user_data) > 1:
            raise MultipleValueReturned
        if user_data is None:
            return None
        if user_data.get("password") == cls.__hash_password(password):
            primary_key = user_data.get("pk")
            username = user_data.get("username")
            user = User(primary_key, username)
            return user
        return None
