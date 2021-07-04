import argparse
import time
from collections import namedtuple

from src import auth
from src.db_manager import db
from src.halo_logger import logger

parser = argparse.ArgumentParser(description="Process input and output files.")
parser.add_argument(
    "input_file",
    metavar="input file",
    type=open,
    help="input file for the Halo Software",
)
parser.add_argument(
    "output_file",
    metavar="output file",
    type=str,
    help="output file for the Halo Software",
)
parser.add_argument(
    "bonus",
    metavar="handle case",
    type=int,
    help="handle case for the Halo Software",
)

args = parser.parse_args()


class Command:
    def __init__(self, name, *args):
        self.name = name
        self.set_options(*args)
        self._command = f"{name} {' '.join(args)}"

    def exce(self):
        raise NotImplemented

    def set_options(self, *args):
        raise NotImplemented


class AuthCommand(Command):
    def set_options(self, *args):
        if self.name.upper() == "REGISTER":
            self._type, self.username, self.password, self.re_password = args
        elif self.name.upper() == "LOGIN":
            self.username, self.password = args

    def exce(self, user=None):
        if self.name.upper() == "REGISTER":
            auth.UserManager.create_user(self.username, self.password, self.re_password)
        elif self.name.upper() == "LOGIN":
            user = auth.UserManager.authenticate(self.username, self.password)
        elif self.name.upper() == "LOGOUT":
            logger.info(f"{user.username},{int(time.time())},{self._command},SUCCESS")
            user = None
        return user

    @property
    def has_output(self, cmd):
        return False


class DLOCommand(Command):
    def set_options(self, *args):
        if self.name.upper() == "CREATE":
            self._type, self.type_name, self.count, *self.fields = args
        elif self.name.upper() == "DELETE":
            self._type, self.type_name = args
        elif self.name.upper() == "INHERIT":
            self._type, self.type_name, self.type_target, *self.fields = args
        elif self.name.upper() == "LIST":
            self._type = args

    def exce(self):
        data = None
        if self.name.upper() == "CREATE":
            db.create_type(self.type_name, *self.fields)
        elif self.name.upper() == "DELETE":
            db.delete_type(self.type_name)
        elif self.name.upper() == "INHERIT":
            db.inherit_type(self.type_name, self.type_target, *self.fields)
        elif self.name.upper() == "LIST":
            data = db.list_type()
        db.commit()
        return data

    @property
    def has_output(self):
        return self.name.upper() == "LIST"


class MLOCommand(Command):
    def set_options(self, *args):
        if self.name.upper() == "CREATE":
            self.recored, self.type_name, self.primary_key, *self.values = args
        elif self.name.upper() == "DELETE":
            self.recored, self.type_name, self.primary_key = args
        elif self.name.upper() == "UPDATE":
            self.recored, self.type_name, self.primary_key, *self.values = args
        elif self.name.upper() == "SEARCH":
            self.recored, self.type_name, self.primary_key = args
        elif self.name.upper() == "LIST":
            self.recored, self.type_name = args
        elif self.name.upper() == "FILTER":
            self.recored, self.type_name, self.filed, self.operator, self.value = args

    def exce(self):
        data = None
        if self.name.upper() == "CREATE":
            db.create_recored(self.type_name, *self.values, primary_key=self.primary_key)
        elif self.name.upper() == "DELETE":
            db.delete_recored(self.type_name, self.primary_key)
        elif self.name.upper() == "UPDATE":
            db.update_recored(self.type_name, self.primary_key, *self.values)
        elif self.name.upper() == "SEARCH":
            data = db.search_recored(self.type_name, self.primary_key)
        elif self.name.upper() == "LIST":
            data = db.list_recoreds(self.type_name)
        elif self.name.upper() == "FILTER":
            data = db.filter_recoreds(
                self.type_name, self.filed, self.value, self.operator
            )
        db.commit()
        return data

    @property
    def has_output(self):
        return self.name.upper() in ["SEARCH", "LIST", "FILTER"]


class HaloSoftware:
    user = None
    AUTH_CMD = ["REGISTER", "LOGIN", "LOGOUT"]
    DLO_CMD = ["CREATE TYPE", "DELETE TYPE", "INHERIT TYPE", "LIST TYPE"]
    MLO_CMD = [
        "CREATE RECORD",
        "DELETE RECORD",
        "UPDATE RECORD",
        "SEARCH RECORD",
        "LIST RECORD",
        "FILTER RECORD",
    ]

    def _get_dumy_user(self, username):
        return auth.User(None, username
            )
    def __init__(self):
        self.input_file = args.input_file
        self.output_file = args.output_file
        self.is_bonus = bool(args.bonus)
        self.user = self._get_dumy_user('Admin') if self.is_bonus else None
        self.commands = self.__parse_commands(self.input_file)
        self.exce(self.commands)

    def __parse_commands(self, file):
        lines = [line.split() for line in file.readlines()]
        data = []
        for line in lines:
            cmd_name = line[0]
            if cmd_name.upper() in self.AUTH_CMD:
                cmd = AuthCommand(cmd_name, *line[1:])
            elif f"{cmd_name} {line[1]}".upper() in self.DLO_CMD:
                cmd = DLOCommand(cmd_name, *line[1:])
            elif f"{cmd_name} {line[1]}".upper() in self.MLO_CMD:
                cmd = MLOCommand(cmd_name, *line[1:])
            data.append(cmd)
        return data

    def exce(self, commands):
        with open(f"{self.output_file}", "w") as file:
            for cmd in self.commands:
                if isinstance(cmd, AuthCommand):
                    self.user = cmd.exce(self.user)
                elif (
                    isinstance(cmd, DLOCommand) or isinstance(cmd, MLOCommand)
                ) and self.user is None:
                    logger.error(f"NULL,{int(time.time())},{cmd._command},FAILURE")
                elif isinstance(cmd, DLOCommand) or isinstance(cmd, MLOCommand):
                    opt = cmd.exce()
                    if cmd.has_output:
                        if isinstance(cmd, DLOCommand) and cmd.name.upper() == "LIST":
                            if opt:
                                file.write(f"E226-S187, ")
                            for key in opt.keys():
                                file.write(f"{key}\n")
                        elif (
                            isinstance(cmd, MLOCommand) and cmd.name.upper() == "SEARCH"
                        ):
                            if opt:
                                file.write(f"E226-S187, ")
                            for value in opt.values():
                                file.write(f"{value}, ")
                            file.write("\n")
                        elif isinstance(cmd, MLOCommand) and (
                            cmd.name.upper() == "LIST" or cmd.name.upper() == "FILTER"
                        ):
                            if opt:
                                file.write(f"E226-S187, ")
                            for key, values in opt.items():
                                if isinstance(values, dict):
                                    file.write(f'{key}, ')
                                    for value in values.values():
                                        file.write(f"{value}, ")
                                else:
                                    file.write(f"{values}, ")
                            file.write("\n")

                    logger.info(
                        f"{self.user.username},{int(time.time())},{cmd._command},SUCCESS"
                    )


if __name__ == "__main__":
    hallo = HaloSoftware()
