import re

class Message:
	rfc2812 = r'^(?::(([^@!\ ]*)(?:(?:!([^@]*))?@([^\ ]*))?)\ )?([^\ ]+)((?:\ [^:\ ][^\ ]*){0,14})(?:\ :?(.*))?$'
	pattern = re.compile(rfc2812)
	ctcp_pattern = re.compile(r"^\x01(.*)\x01$")
	def __init__(self,text):
		self.raw = text
		match = re.match(Message.pattern,text)
		self.prefix = match.group(1)
		self.nick = match.group(2)
		self.user = match.group(3)
		self.host = match.group(4)
		self.command = match.group(5)
		self.parameters = match.group(6).strip().split(" ")
		self.message = match.group(7)
		self.original = match.group(7)
		self.sender = None
		self.replyto = None
		self.channel = None
		self.is_ctcp = False
		self.is_action = False
		if self.command.upper() in ("PRIVMSG","NOTICE"):
			self.sender = self.nick
			if self.parameters[0].startswith('#'):
				self.replyto = self.parameters[0]
				self.channel = self.parameters[0]
			else:
				self.replyto = self.nick
			if self.message:
				ctcp_match = Message.ctcp_pattern.match(self.message)
				if ctcp_match:
					self.is_ctcp = True
					if ctcp_match.group(1).split(" ",1)[0].upper() == "ACTION":
						self.is_action = True
			if self.is_ctcp:
				self.message = ctcp_match.group(1)
				self.original = ctcp_match.group(1)
			if self.is_action:
				self.message = self.message.replace("ACTION ","")
