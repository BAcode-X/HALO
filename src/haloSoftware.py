import argparse
from auth import User, UserManager
from type import Type
from core import Record
import time
import csv
from exceptions import InvalidCreaditioal

class Halo:

    user = None
    status = 'failure'

    def __init__(self):
        with open('halodb.csv', 'w') as f:
            pass
        with open('haloLog.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'occurance', 'operation', 'status'])

    def record_log(self, list):
        with open('haloLog.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list)

    
    def run(self, input_file):
        file = open(f'{input_file}', 'r+', newline='')
        for i in file:
            if i:
                cmd = str(i).strip().split()
                if len(cmd) != 1:
                    if cmd[0] == 'create' and cmd[1] == 'type':
                        type_obj = Type()
                        type_obj.create(cmd[2], cmd[3], cmd[4:])
                        self.status = 'success'
                    elif cmd[0] == 'login':
                        self.user = UserManager.authenticate(cmd[1], cmd[2])
                        self.status = 'success' if self.user else 'failure'
                    elif cmd[0] == 'register':
                        try:
                            UserManager.create_user(cmd[2], cmd[3], cmd[4])
                        except:
                            self.status = 'failure'
                    elif cmd[0] == 'delete':
                        pass

                else:
                    self.user = None
                    self.status = 'success'

                log = [self.user.username if self.user else 'null']
                log.append(''.join(str(time.time()).split('.')))
                log.append(' '.join(cmd))
                log.append(self.status)
                self.record_log(log)


obj = Halo()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file path')
    args = parser.parse_args()

    obj.run(args.input)