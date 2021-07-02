import argparse

from auth import User
from core import Record
from type import Type


class Halo:
    def __init__(self):
        open(
            "haloLog.csv",
        )


if __name__ == "__main__":
    while 1:
        try:
            cmd = input(">> ")
        except:
            break
