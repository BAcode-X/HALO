import json
import uuid
import csv
import os
class Type:
    
    def __init__(self):
        pass

    def create(self, name, number, attrs):
        with open('halodb.csv', 'a') as f:
            writer = csv.writer(f)
            data = [name]
            data += [i for i in attrs]
            for i in range(7-int(number)):
                data.append('')
            print(data)
            writer.writerow(data)

    def delete(self, type_name):
        with open('halodb.csv', 'r') as inp, open('halodb_1.csv', 'w') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[0] != type_name:
                    writer.writerow(row)
        os.remove('halodb.csv')
        os.rename('halodb_1.csv', 'halodb.csv')

    def inherit(self, *args, **kwargs):
        pass

    def list_all(self, *args, **kwargs):
        pass
