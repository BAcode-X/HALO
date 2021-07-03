import argparse
from collections import namedtuple

from src import auth
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_file', metavar='input file', type=open,
                    help='input file for the Halo Software')
parser.add_argument('output_file', metavar='output file', type=str,
                    help='output file for the Halo Software')

args = parser.parse_args()

class Command:

	def __init__(self, name, *args):
		self.name = name
		self.set_options(*args)

	def exce(self):
		pass

	def set_options(self, *args):
		raise NotImplemented

class AuthCommand(Command):

	def set_options(self, *args):
		if self.name.upper() == 'REGISTER':
			self._type, self.username, self.password, self.re_password = args
		elif self.name.upper() == 'LOGIN':
			self.username, self.password = args

	def exce(self):
		if self.name.upper() == 'REGISTER':
			user = auth.UserManager.create_user(self.username, self.password, self.re_password)
		elif self.name.upper() == 'LOGIN':
			user = auth.UserManager.authenticate(self.username, self.password)
		elif self.name.upper() == 'LOGOUT':
			user = None
		return user

class DLOCommand(Command):

	def set_options(self, *args):
		if self.name.upper() == 'CREATE':
			self._type, self.type_name, *self.fields = args
		elif self.name.upper() == 'DELETE':
			self._type, self.type_name = args
		elif self.name.upper() == 'INHERIT':
			self._type, self.type_target, self.type_name, *self.fields = args

	def exce(self):
		if self.name.upper() == 'REGISTER':
			user = auth.UserManager.create_user(self.username, self.password, self.re_password)
		elif self.name.upper() == 'LOGIN':
			user = auth.UserManager.authenticate(self.username, self.password)
		elif self.name.upper() == 'LOGOUT':
			user = None
		return user


class HaloSoftware:

	user = None
	AUTH_CMD = ['REGISTER', 'LOGIN', 'LOGOUT']
	def __init__(self):
		self.input_file = args.input_file
		self.output_file =  args.output_file
		self.commands  = self.__parse_commands(self.input_file)
		self.exce(self.commands)

	def __parse_commands(self, file):
		lines = [line.split() for line in file.readlines()]
		data = []
		for line in lines:
			cmd_name = line[0]
			if cmd_name.upper() in self.AUTH_CMD:
				cmd = AuthCommand(cmd_name, *line[1:])

			data.append(cmd)
		return data

	def exce(self, commands):
		for cmd in self.commands:
			if isinstance(cmd, AuthCommand):
				user = cmd.exce()
			cmd.exce()

if __name__ == '__main__':
	hallo = HaloSoftware()