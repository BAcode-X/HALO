import argparse
from auth import User
from type import Type
from core import Record

class Halo:

    def __init__(self):
        # open('haloLog.csv', 'w+')
        pass
    
    def run(self, input_file):
        print(input_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file path')
    args = parser.parse_args()

    obj = Halo()

    obj.run(args.input)