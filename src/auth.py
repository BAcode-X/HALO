import json
import os
import time
import uuid
from hashlib import pbkdf2_hmac

from db_manager import db
from exceptions import (
    DuplicatedPrimaryKey,
    ForbidenAccess,
    InvalidCreaditioal,
    MultipleValueReturned,
    UniqueConstraintError,
)
from halo_logger import logger


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
            raise ForbidenAccess("cannot set a primary key.")
        if attr not in self.__fields:
            raise ForbidenAccess(f"Setting an attribute '{attr}'' is forbiden.")
        return super().__setattr__(attr, value, *args, **kwargs)

    def __repr__(self):
        return f"<User '{self.username}'>"


class UserManager:
    @classmethod
    def create_user(cls, username, password, new_password):
        if password != new_password:
            logger.error(f"NULL, {int(time.time())}, REGISTER USER {username}, FAILURE")
            raise InvalidCreaditioal("Password mismatched")
        if not username.isalnum():
            logger.error(f"NULL, {int(time.time())}, REGISTER USER {username}, FAILURE")
            raise TypeError("Username must be alphanumeric.")
        hashed_password = cls.__hash_password(password)
        user_data = cls.__create_user(username, hashed_password)
        if user_data is None:
            return None
        user = User(None, None)
        for key, value in user_data.items():
            setattr(user, key, value)
        logger.info(f"NULL, {int(time.time())}, REGISTER, USER, {username}, SUCCESS")
        return user

    @classmethod
    def __create_user(cls, username, hashed_password):
        try:
            user = db.create_recored("users", username, hashed_password)
            db.commit()
            return user
        except (UniqueConstraintError, DuplicatedPrimaryKey):
            logger.error(
                f"NULL, {int(time.time())}, REGISTER, USER, {username}, FAILURE"
            )
        return None

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
        user_data = db.filter_recoreds("users", "username", username, "=")
        if user_data is None:
            logger.error(f"{username}, {int(time.time())}, LOGIN, FAILURE")
            return None
        if user_data.get("password") == cls.__hash_password(password):
            primary_key = user_data.get("primary_key")
            username = user_data.get("username")
            user = User(primary_key, username)
            logger.info(f"{username}, {int(time.time())}, LOGIN, SUCCESS")
            return user
        logger.error(f"{username}, {int(time.time())}, LOGIN, FAILURE")
        return None
