import re
import asyncio
from blinker import signal
import model
from IrcMessage import Message

class IRCProtocol(asyncio.Protocol):
	def __init__(self,name,host,port):
		self.buff = ""
		self.name = name
		self.host = host
		self.port = port

	def connection_made(self,transport):
		self.t = transport
		self.bot = model.Bot(self.name,self.t)
		print("created bot instance")
		self.bot.commands.auth(self.bot.nick)
		print("sent bot-init")

	def data_received(self,data):
		try:
			self.buff += data.decode("UTF-8")
		except UnicodeDecodeError:
			self.buff += data.decode("Latin-1")
		while '\n' in self.buff:
			raw = self.buff.split('\n',1)[0]
			message = Message(raw.strip())
			self.buff = self.buff[self.buff.index('\n')+1:]
			debug_print_line(message)
			self.bot.react_to_message(message)

	def connection_lost(self,exc):
		if exc:
			print("error: {}".format(exc.strerror))
		else:
			print("EOF received")
		signal("SUPER").send(None,act="disconnect",params={
				'name': self.name
				})

def debug_print_line(message):
	ignoredcommands = [
			"PRIVMSG",
			"NOTICE",
			"JOIN",
			"QUIT",
			"PART",
			"__001", #welcome
			"002", #your host
			"003", #server creation
			"004", #your info
			"005", #supported commands
			"251", #user count
			"252", #operator count
			"254", #channel count
			"255", #client/server count
			"301", #user is away
			"305", #marked as back
			"306", #marked as away
			"332", #channel topic
			"333", #topic who/time
			"353", #RPL_NAMREPLY
			"366", #RPL_ENDOFNAMES
			"372", #motd
			"396", #your host hidden successfully
			"422", #missing motd
			"PING",
			"NICK",
			"MODE"
		]
	if message.command not in ignoredcommands:
		print(message.raw)
