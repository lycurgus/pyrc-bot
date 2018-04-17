#!/usr/bin/env python3

import sys
import re

class Editor:
	command_pattern = re.compile(r"(\d*)(,?)(\d*)([qrepwa])(?: (.*))?")
	def __init__(self,filename=None):
		self.buff = []
		self.cursor = 0
		self.filename = filename
		if filename:
			with open(filename,"r") as f:
				self.buff = f.read()

	def read(self,filename=None):
		if not (self.filename or filename):
			return None
		o = filename if filename else self.filename
		with open(o,"r") as f:
			self.buff = []
			for line in f.read():
				self.buff.append(line)

	def write(self,filename=None):
		if not (self.filename or filename):
			print("no filename")
			return None
		o = filename if filename else self.filename
		with open(o,"w") as f:
			for line in self.buff:
				f.write(line+'\n')

	def edit(self,c=None):
		line = input()
		if not c:
			c = self.cursor
		temp = []
		while line != ".":
			temp.append(line)
			line = input()
		self.buff = self.buff[:c] + temp + self.buff[c:]
		self.cursor += len(temp)

	def print(self,f=None,t=None):
		if not f:
			f = 1
		if not t:
			t = len(self.buff)
		for line in self.buff[f:t]:
			print(line)

	def command(self,i=None):
		if not i:
			i = input()
		command_match = Editor.command_pattern.match(i)
		if not command_match:
			print("?")
			return
		try:
			first_c = int(command_match.group(1))
		except ValueError:
			first_c = None
		comma = command_match.group(2)
		try:
			second_c = int(command_match.group(3))
		except ValueError:
			second_c = None
		command = command_match.group(4)
		argument = command_match.group(5)
		print("first: {}\ncomma: {}\nsecond: {}\ncommand: {}\nargument: {}".format(first_c,comma,second_c,command,argument))
		if command == "p":
			self.print(first_c,second_c)
		elif command == "q":
			sys.exit()
		elif command == "a":
			self.edit(first_c)
		elif command == "w":
			self.write(argument)

	def run(self):
		while True:
			i = input()
			self.command(i)
			print(self.buff)

if __name__ == "__main__":
	e = Editor()
	e.run()
