import colours

class IRCQueuedCommands:
	def __init__(self,queue):
		self.queue = queue

	def raw(self,message,wait):
		for c in ("\r","\n"):
			message = message.replace(c, "")
		if not message.startswith("PONG"):
			print("sending raw: {}".format(message))
		self.queue.put(('{}\r\n'.format(message).encode('UTF-8'),wait))

	def send(self,command,payload,wait=0):
		self.raw("{} {}".format(command,payload),wait)

	def pong(self,payload):
		self.send("PONG",payload)

	def irc_pass(self,password):
		self.send("PASS",password)

	def nick(self,nick):
		self.send("NICK",nick)

	def user(self,ident,mode):
		if mode != 0 and mode != 8:
			mode = 8
		self.send("USER","{0} {1} serv :{0}".format(ident,mode))

	def auth(self,nick,mode=8):
		self.nick(nick)
		self.user(nick,mode)

	def privmsg(self,target,message,nowait=False):
		message = colours.replace(message)
		delay = 0
		if not nowait:
			delay = len(message)*0.1
		self.send("PRIVMSG","{} :{}".format(target,message),delay)

	def notice(self,target,message):
		self.send("NOTICE","{} :{}".format(target,message))

	def join(self,channel):
		if channel:
			if not channel.startswith("#"):
				channel = "#" + channel
			self.send("JOIN",channel)

	def multijoin(self,channel_list):
		for channel in channel_list:
			self.join(channel)

	def part(self,channel):
		if channel:
			if not channel.startswith("#"):
				channel = "#" + channel
		self.send("PART",channel)

	def names(self,channellist):
		self.send("NAMES",",".join(channellist))

	def away(self,message):
		self.send("AWAY",":{}".format(message))

	def unaway(self,my_nick):
		self.send(":{}".format(my_nick),"AWAY")

	def quit(self,reason="quitting"):
		self.send("QUIT",":{}".format(reason))

	def ctcp_ask(self,target,ctcp_type):
		self.privmsg(target,"\x01{}\x01".format(ctcp_type))

	def ctcp_reply(self,target,ctcp_type,reply_string):
		self.notice(target,"\x01{0} {1}\x01".format(ctcp_type,reply_string))

	def action(self,target,action):
		self.privmsg(target,"\x01ACTION {}\x01".format(action))

	def dcc_offer(self,target,filename,filesize,my_ip_int,port):
		self.privmsg(target,"\x01DCC SEND {0} {1} {2} {3}\x01".format(filename,my_ip_int,port,filesize))

	def whois(self,nick):
		self.send("WHOIS",nick)
