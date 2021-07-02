import os
import uuid
import json

from hashlib import pbkdf2_hmac

from exceptions import InvalidCreaditioal

class User:
    primary_key = None
    username = None
    password = None
    __fields = ['primary_key', 'username', 'password']

    def __init__(self, primary_key, username):
        self.primary_key = primary_key
        self.username = username

    def __setattr__(self, attr, value, *args, **kwargs):
        if attr not in self.__fields:
            raise KeyError(f"Setting an attribute '{attr}'' is forbiden.")
        return super().__setattr__(attr, value, *args, **kwargs)

    def __str__(self):
        return self.primary_key.hex

class UserManager:
    
    @classmethod
    def create_user(cls, username, password, new_password):
        if password != new_password:
            raise InvalidCreaditioal("Password mismatched")
        if not username.isalnum():
            raise TypeError("Username must be alphanumeric.")
        user = User()
        setattr(user, 'username', username)
        setattr(user, 'password', cls.hash_password(password))

        return user

    @classmethod
    def hash_password(cls, password):
        hashed_password = pbkdf2_hmac('sha256', f'password'.encode(), os.urandom(10), 100000)
        return hashed_password.hex()


    @classmethod
    def __filter_primary_key(cls, username):
            with open('users.json', 'r') as f:
                users = json.load(f)
                users.get(username, None)


    @classmethod
    def authenticate(cls, username, password):
        pass