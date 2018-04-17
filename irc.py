import re
import asyncio
from blinker import signal
import model

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
		#signal("BOT-init").send(self,bot=self.bot)
		self.bot.commands.auth(self.bot.nick)
		print("sent bot-init")

	def data_received(self,data):
		try:
			self.buff += data.decode("UTF-8")
		except UnicodeDecodeError:
			self.buff += data.decode("Latin-1")
		while '\n' in self.buff:
			raw = self.buff.split('\n')[0]
			line = IRCLine(raw.strip())
			message = IRCMessage(line)
			self.buff = self.buff[self.buff.index('\n')+1:]
			#signal("LINE").send(self,line=line,bot=self.bot)
			#self.bot.react_to_line(line)
			self.bot.react_to_line(line,message)
			#signal(line.command).send(self,line=line,bot=self.bot)
			debug_print_line(line)

	def connection_lost(self,exc):
		if exc:
			print("error: {}".format(exc.strerror))
		else:
			print("EOF received")
		signal("SUPER").send(None,act="disconnect",params={
				'name': self.name
				})

def debug_print_line(line):
	ignoredcommands = [
			"PRIVMSG",
			"NOTICE",
			"JOIN",
			"QUIT",
			"PART",
			"__001", #welcome
			"002", #your host
			"003", #server creation
			"004", #???
			"005", #supported commands
			"251", #user count
			"252", #operator count
			"254", #channel count
			"255", #client/server count
			"301", #user is away
			"305", #marked as back
			"306", #marked as away
			"332",
			"333",
			"353",
			"366",
			"372",
			"396",
			"422", #missing motd
			"PING",
			"NICK",
			"___MODE"
		]
	if line.command not in ignoredcommands:
		print(line.line['raw'])

class IRCLine:
	rfc2812 = r'^(?::(([^@!\ ]*)(?:(?:!([^@]*))?@([^\ ]*))?)\ )?([^\ ]+)((?:\ [^:\ ][^\ ]*){0,14})(?:\ :?(.*))?$'
	pattern = re.compile(rfc2812)
	def __init__(self,string):
		match = re.match(IRCLine.pattern,string)
		prfx = match.group(1)
		nick = match.group(2)
		user = match.group(3)
		host = match.group(4)
		cmmd = match.group(5)
		prms = match.group(6).strip().split(" ")
		rest = match.group(7)
		self.line = {
				"raw": string,
				"prefix": prfx,
				"nick": nick,
				"user": user,
				"host": host,
				"command": cmmd,
				"parameters": prms,
				"rest": rest
				}
		self.message = None
		self.prefix = prfx
		self.nick = nick
		self.user = user
		self.host = host
		self.command = cmmd
		self.parameters = prms
		self.rest = rest
		if self.command in IRCMessage.messageTypes:
			self.message = IRCMessage(self)

class IRCMessage:
	messageTypes = ("PRIVMSG","NOTICE")
	ctcp_pattern = re.compile(r"^\x01(.*)\x01$")
	def __init__(self,line):
		self.line = line
		self.command = line.command
		self.sender = line.nick
		self.message = line.rest
		self.original = line.rest
		if line.parameters[0].startswith('#'):
			self.replyto = line.parameters[0]
			self.channel = line.parameters[0]
		else:
			self.replyto = line.nick
			self.channel = None
		ctcp_match = IRCMessage.ctcp_pattern.match(self.line.rest) if self.line.rest else None
		self.is_ctcp = True if ctcp_match else False
		if self.is_ctcp:
			self.message = ctcp_match.group(1)
			self.original = ctcp_match.group(1)
		self.is_action = False
		if ctcp_match:
			self.is_action = True if ctcp_match.group(1).split(" ",1)[0] == "ACTION" else False
			if self.is_action:
				self.message = self.message.replace("ACTION ","")
				#self.original = self.original.replace("ACTION ","")
