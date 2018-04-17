import asyncio
from blinker import signal
from irc import IRCProtocol

class Connection:
	def __init__(self,host,port,task,auto=False,bot=None):
		self.host = host
		self.port = port
		self.task = task
		self.auto = auto
		self.bot = bot

class Supervisor:
	def __init__(self, loop):
		self.connections = {}
		self.loop = loop
		self.idlecount = 0
		sig_supervisor = signal("SUPER")
		def supervisor_act(sender,**kwargs):
			act = kwargs['act']
			p = kwargs['params']
			f = getattr(self,act,None)
			if f:
				f(p)
			else:
				print("supervisor got unrecognised command: {}".format(act))
		self.supervisor_act = supervisor_act
		sig_supervisor.connect(self.supervisor_act)
		sig_tick = signal("TICK-base")
		def watchdog(sender,**kwargs):
			#count = len(asyncio.Task.all_tasks(self.loop))
			count = len(self.connections) #TODO confirm this is workable
			if count == 0:
				self.idlecount += 1
			if self.idlecount >= 5:
				self.loop.call_soon_threadsafe(self.loop.stop)
		self.watchdog = watchdog
		sig_tick.connect(self.watchdog)

	def connect(self,params):
		name = params['name']
		host = params['host']
		port = params['port']
		protocol = IRCProtocol(name,host,port)
		task = asyncio.ensure_future(self.loop.create_connection(lambda: protocol,host,port))
		#TODO if the connect throws an exception we would like to catch it
		#TODO might be feasible to call the exception() method of the task? will need to catch InvalidStateError and CancelledError (potentially) until either an exception or None is returned by the function
		self.connections[name] = Connection(host,port,task,True,None)
		for c in self.connections.keys():
			print("connections: {}".format(repr(self.connections[c])))

	def disconnect(self,params):
		name = params['name']
		if name not in self.connections.keys():
			return None
		host = self.connections[name].host
		port = self.connections[name].port
		auto = self.connections[name].auto
		if not self.connections[name].bot.quit:
			self.connections[name].bot.commands.quit()
		del self.connections[name]
		if auto:
			print('reconnecting')
			self.connect({
				'name': params['name'],
				'host': host,
				'port': port
				})

	def set_auto(self,params):
		name = params['name']
		if name in self.connections.keys():
			self.connections[name].auto = params['auto']

	def bot_instance(self,params):
		name = params['name']
		bot = params['bot']
		if not self.connections[name].bot:
			self.connections[name].bot = bot
