import json
import os
import uuid
from hashlib import pbkdf2_hmac

from exceptions import InvalidCreaditioal


class User:
    planet = "E226-S187"
    primary_key = None
    username = None
    USERNAME, PASSWORD, PRIMARY_KEY = "username", "password" ,"primary_key"
    __fields = [PRIMARY_KEY, USERNAME, PASSWORD]

    def __init__(self, primary_key, username):
        self.primary_key = primary_key
        self.username = username

    def __setattr__(self, attr, value, *args, **kwargs):
        if attr not in self.__fields:
            raise KeyError(f"Setting an attribute '{attr}'' is forbiden.")
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
        # NO REP USERNAME
        user = User(5, None)
        setattr(user, User.USERNAME, username)
        hashed_password = cls.hash_password(password)
        cls.__create_user(5, username, hashed_password)
        return user

    @classmethod
    def __create_user(cls, pk, username, hashed_password):
        json_data = cls.__get_all_users()
        with open("users.json", "w") as f:
            json_data.update({pk: {User.USERNAME: username, User.PASSWORD: hashed_password}})
            json.dump(json_data, f)

    @classmethod
    def __get_all_users(cls):
        json_data = None
        with open("users.json", "r") as f:
            json_data = json.load(f)
        return json_data

    @classmethod
    def hash_password(cls, password):
        hashed_password = pbkdf2_hmac(
            "sha256", f"{password}".encode(), b"3cd83f359b2e8db6a3b0", 100000
        )
        return hashed_password.hex()

    @classmethod
    def __filter_username(cls, username):
        with open("users.json", "r") as f:
            users = json.load(f)
            for user_pk in users:
                if users[user_pk][User.USERNAME] == username:
                    return {
                        "pk": user_pk,
                        User.USERNAME: username,
                        User.PASSWORD: users[user_pk].get("password"),
                    }
        return None

    @classmethod
    def authenticate(cls, username, password):
        user_data = cls.__filter_username(username)
        if user_data is None:
            return False
        if user_data.get("password") == cls.hash_password(password):
            primary_key = user_data.get("pk")
            username = user_data.get("username")
            user = User(primary_key, username)
            return user
        return False
