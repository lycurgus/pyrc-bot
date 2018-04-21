import time
import os
import sys
import sqlite3
import re
import queue
import threading
import datetime
import random
from IrcQueuedCommands import IRCQueuedCommands
from blinker import signal
from util import random_characters, reload, hours, minutes, days, Timer, listify, chance, lower
import math

class Bot:
	def __init__(self,servername,transport):
		self.ignoreautojointemp = ["#limittheory","#r/linux"]
		self.ignoreautojointemp = []
		self.servername = servername
		self.debug = False
		self.connected = False
		self.ns_registered = False
		self.ns_ident_sent = False
		self.quit = False
		self._flags = {}
		self.channels = {}
		self.modes = []
		self.servermodes = {}
		self.channels_awaiting_auth = []
		self.timers = {}
		self.counters = {}
		self.seen_users = {}
		self.expectations = []
		self.tick = 0
		sig_tick = signal("TICK-base")
		def handle_tick(sender,**kwargs):
			self.clock_tick(kwargs["d"])
		self.handle_tick = handle_tick
		print(list(sig_tick.receivers_for(sig_tick)))
		if not self.handle_tick in sig_tick.receivers_for(sig_tick):
			print("registering tick handler for {}".format(self.servername))
			sig_tick.connect(self.handle_tick) #TODO will this affect subsequent bot instances....?
		else:
			print("tick handler for {} already registered!".format(self.servername))
		self.transport = transport #outgoing to IRC
		self.queue = queue.Queue() #incoming from channels
		self.commands = IRCQueuedCommands(self.queue)
		self.gmtoffset = -(time.altzone if (time.daylight and time.localtime().tm_isdst > 0) else time.timezone) #seconds
		self.db = None
		self.get_db('snuggles.sqlite')
		self.get_config()
		# new stuff v
		self.queued_actions = []
		self.functions = {}
		self.modules = set() #TODO replace all references to self.functions with self.modules - each entry should instead be a LoadedModule (name and list of functions)
		#TODO or should modules/functions still be a dict, but replace timeouts/timed_functions with sets??
		self.timeouts = {}
		self.timed_functions = {}
		self.loadedmodules = []
		self.failedmodules = []
		self.load_modules()
		# new stuff ^
		self.run()

	def clock_tick(self,delta):
		self.tick += delta
		tick_num = int(round(self.tick/delta))
		if self.debug:
			if (tick_num % 2):
				print('tick!')
			else:
				print('tock!')
		for timer in self.timers.values():
			t = timer[0]
			m = timer[1]
			if (tick_num % t.timer == 0):
				for function in self.timed_functions[t.name]:
					function[0](self,None,None)
		if tick_num == (1000000/delta):
			print("tick reached 1000000, resetting to 0")
			self.tick = 0

	def register_handler(self,function,module):
		if not module in self.functions.keys():
			self.functions[module] = []
		self.functions[module].append(function)

	def register_timed_function(self,function,module):
		timername = getattr(function,"timer")
		if timername not in self.timed_functions.keys():
			self.timed_functions[timername] = []
		self.timed_functions[timername].append((function,module))

	def register_timer(self,timer,module):
		if timer.name in self.timers.keys():
			del self.timers[timer.name]
#		else:
#			self.timed_functions[timer.name] = []
		self.timers[timer.name] = (timer,module)

	def register_timeout(self,timeout,module):
		if timeout.name in self.timeouts.keys():
			del self.timeouts[timeout.name]
		self.timeouts[timeout.name] = (timeout,module)
		print("timeout registered: {}".format(self.timeouts[timeout.name]))

	def load_modules(self):
		for module_file in os.listdir('modules'):
			if module_file.endswith('.py'):
				module_name = module_file.replace('.py','')
				self.load_module(module_name)

	def reload_all_modules(self):
		for module in self.functions.keys():
			self.reload_module(module)

	def load_module(self,module):
		if module in self.functions.keys():
			print("module {} already loaded!".format(module))
			return
		import importlib
		#print("loading module {}".format(module))
		try:
			m = importlib.import_module("modules.{}".format(module))
		except:
			print("unable to load module {}".format(module))
			import sys, traceback
			ex_type, ex, tb = sys.exc_info()
			traceback.print_tb(tb)
			print(ex)
		else:
			importlib.reload(m)
			print('loading {}'.format(module))
			mc = getattr(m,module,None)
			if mc:
				mc.initialise(self)
				if module in self.failedmodules:
					self.failedmodules.remove(module)
				self.loadedmodules.append(module)
			else:
				self.failedmodules.append(module)
				raise Exception("module {} does not define a properly-named module instance!".format(mc))

	def unload_module(self,module):
		print('unloading {}'.format(module))
		if module in self.failedmodules:
			self.failedmodules.remove(module)
		if module in self.loadedmodules:
			self.loadedmodules.remove(module)
		if module in self.functions.keys():
			del self.functions[module]
		#print(repr(self.timed_functions))
		#unload timed functions
		self.timed_functions = {k: [tf for tf in tfs if tf[1] is not module] for k, tfs in self.timed_functions.items()}
		#unload timers
		self.timers = {k: (tr[0],tr[1]) for k, tr in self.timers.items() if tr[1] is not module}
		#unload timeouts
		self.timeouts = {k: (to[0],to[1]) for k, to in self.timeouts.items() if to[1] is not module}
		#ensure reloader and core are always loaded
		if "reloader" not in self.functions.keys():
			self.load_module("reloader")
		if "core" not in self.functions.keys():
			self.load_module("core")

	def reload_module(self,module):
		print("reloading {}".format(module))
		self.unload_module(module)
		self.load_module(module)

	def react_to_line2(self,line,message=None):
		self.check_expectations(line)
		for module in self.modules[:]:
			functions = module.check_triggers(message,self)
			for fn in functions:
				if hasattr(fn,"line"):
					fn[0](self,line,fn[1])
				else:
					fn[0](self,message,fn[1])

	def react_to_line(self,line,message=None):
		self.check_expectations(line)
		for f in list(self.functions.values())[:]:
			for fn in f:
				#check = self.check_trigger(fn,line)
				check = self.check_trigger(fn,message)
				if check[0]:
					if hasattr(fn,"line"):
						fn(self,line,check[1])
					else:
						if False:
							print("fn")
							print(type(fn))
							print(repr(fn))
							print("self")
							print(type(self))
							print(repr(self))
							print("message")
							print(type(message))
							print(repr(message))
							print("check")
							print(type(check))
							print(repr(check))
						fn(self,message,check[1])

	def check_trigger(self,function,message):
		#print('---------trigger check for {}'.format(function.__name__))
		possible_attributes = [
				"timeout",
				"type",
				"sender",
				"sender-not",
				"sender-admin",
				"sender-not-admin",
				"channel",
				"channel-not",
				"user-not-present",
				"command","mention",
				"address",
				"direct",
				"regex",
				"action",
				"disable"
			]
		checks = []
		checknames = []
		match = None
		if not message.message:
			return (False,None) #TODO fix this
		#print("function {} has attributes {}".format(function.__name__," ".join([attrib for attrib in dir(function) if not attrib.startswith("__")])))
		check_attributes = list(set(possible_attributes).intersection(dir(function)))
		if "direct" in check_attributes:
			check_attributes.remove("direct")
			check_attributes.insert(0,"direct")
		for a in check_attributes:
			if hasattr(function,a):
				checknames.append(a)
				at = getattr(function,a,None)
				#print("function {} has attribute {}: checking for match".format(getattr(function,"__name__"),a))
				if a == "direct":
					checks.append(self.being_addressed(message.line))
					if any([message.message.startswith(bn.lower()) for bn in self.names]):
						print('original message: {}'.format(message.original))
						message.message = re.sub(r'{}(?:[:, ])?'.format('|'.join(self.names)),'',message.original,count=1,flags=re.IGNORECASE)
						print('altered message: {}'.format(message.message))
				elif a == "timeout":
					checks.append(self.timeout(at).get())
				elif a == "type":
					checks.append(message.command in at)
				elif a == "sender":
					checks.append(message.sender in at)
				elif a == "sender-not":
					checks.append(message.sender not in at)
				elif a == "sender-admin":
					checks.append(self.is_admin(message.sender))
				elif a == "sender-not-admin":
					checks.append(not self.is_admin(message.sender))
				elif a == "channel":
					checks.append(message.channel in at)
				elif a == "channel-not":
					checks.append(message.channel not in at)
				elif a == "user-present":
					if message.channel:
						checks.append(any([u.lower() in list(map(str.lower, self.channels[message.channel].users.keys())) for u in at]))
						#checks.append(any([u.lower() in [cu.lower() for cu in self.channels[message.channel].users.keys()] for u in at]))
					else:
						checks.append(False)
				elif a == "user-not-present":
					if message.channel:
						checks.append(all([u.lower() not in lower(self.channels[message.channel].users.keys()) for u in at]))
					elif message.sender:
						if message.sender.lower() in lower(at):
							checks.append(False)
					else:
						checks.append(True)
				elif a == "mention":
					checks.append(any([bn in message.message for bn in self.names]))
				elif a == "address":
					checks.append(any([any((message.message.startswith(bn),line.rest.endswith(bn))) for bn in self.names]))
				elif a == "action":
					action = re.match(r"^\x01(.*)\x01$",message.original)
					if action:
						#print("action: {}".format(action.group(1).upper().startswith("ACTION")))
						checks.append(action.group(1).upper().startswith("ACTION"))
						message.original = re.sub(r'ACTION ','',action.group(1),count=1)
					else:
						#print("not action")
						checks.append(False)
				elif a == "regex":
					#match = at.match(message.message)
					match = at.match(message.original)
					if match:
						print('regex match for message {}'.format(message.message))
						print('matched against original {}'.format(message.original))
					checks.append(True if match else False)
				elif a == "command":
					c_r = at[1] if at[1] else 0
					c_o = at[2] if at[2] else 0
					cn = '|'.join(at[0]) if isinstance(at[0],list) else at[0]
					c = r"(?:{})\ ?(?:.*\ ?){{{},{}}}".format(cn,str(c_r),str(c_r+c_o))
					command_pattern = re.compile(c,flags=re.IGNORECASE)
					match = command_pattern.match(message.message)
					checks.append(True if match else False)
				elif a == "disable":
					checks.append(False)
		#print("there were {} checks and {} of them were True".format(len(checks),len([c for c in checks if c == True])))
		if function.__name__ == "gift_react":
			print("function {} results:".format(function.__name__))
			print(" ".join(list(map(str,checks))))
			print(" ".join(list(map(str,checknames))))
		if getattr(function,"any",False):
			return (any(checks),match)
		else:
			return (all(checks),match)

	def is_admin(self,nick):
		r = False
		if nick == self.boss: #TODO broader check!
			r = True
		return r

	def queue_action(self,delay,func):
		trigger_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
		self.queued_actions.append((trigger_time,func))

	#def __getattr__(self,attr):
	#	return self.customvalues[attr]
	def getcustom(self,name):
		if not getattr(self,'customvalues',False):
			self.customvalues = {}
		if name in self.customvalues.keys():
			return self.customvalues[name]
		return None

	#def registercustom(self,name,default):
	#	if not getattr(self,'customvalues',False):
	#		self.customvalues = {}
	#	if name in self.customvalues.keys():
	#		print('woah! tried to register a custom attribute ({}) twice'.format(name))
	#	self.customvalues[name] = default

	def removecustom(self,name):
		del self.customvalues[name]

	def setcustom(self,name,value):
		if not getattr(self,'customvalues',False):
			self.customvalues = {}
		self.customvalues[name] = value

	def check_actions(self):
		for i,action in enumerate(self.queued_actions):
			if action[0] < datetime.datetime.now():
				action[1]()
				self.queued_actions[i][0] = False
		self.queued_actions[:] = [a for a in self.queued_actions if a]

	def check_timers(self): #this should be basically the same as clock_tick
		for t in self.timers.items():
			if self.tick:
				pass

	def get_config(self):
		#self.db = None
		if not self.db:
			print("no db!")
			sys.exit(0)
			return None
		c = self.db.cursor()
		c.row_factory = sqlite3.Row
		s = c.execute('SELECT id FROM servers WHERE name = (?)',[self.servername]).fetchone()
		r = c.execute('SELECT id,nick,boss,bedtime,waketime,ns_pass FROM identities WHERE serverId = (?)',[s['id']]).fetchone()
		self.nick = r['nick']
		print("got nick '{}' for myself from identity '{}'".format(self.nick,r['id']))
		self.boss = r['boss']
		self.ns_pass = None if r['ns_pass'] == '' else r['ns_pass']
		self.bedtime = int(r['bedtime'])
		self.waketime = int(r['waketime'])
		ac = c.execute('SELECT name FROM channels WHERE serverId = (?) AND auto = 1',[s['id']]).fetchall()
		self.autochannels = []
		for chan in ac:
			self.autochannels.append(chan['name'])
		p = c.execute('SELECT name FROM petnames WHERE identityId = (?)',[r['id']]).fetchall()
		self.petnames = []
		for pn in p:#.items():
			self.petnames.append(pn['name'])
		self.names = [self.nick] + self.petnames
		#ci = c.execute('SELECT ti.name AS name,ti.days AS days,ti.hours AS hours,ti.minutes AS minutes,ti.seconds AS seconds,ti.enabled AS enabled FROM tickIntervals ti INNER JOIN tickIntervalMappings tim ON ti.id = tim.intervalId WHERE tim.identityId = (?)',[r['id']]).fetchall()
		#self.clockintervals = {}
		#for cv in ci:
		#	self.clockintervals[cv['name']] = TickInterval((days(cv['days'])+hours(cv['hours'])+minutes(cv['minutes'])+cv['seconds']),bool(cv['enabled']))

	def timer(self,name):
		return self.timer_new(name) #TODO confirm this swap didn't break anything
		if not (name in self.timers.keys()):
			self.timers[name] = Timer()
		return self.timers[name]

	def timer_new(self,name):
		if not (name in self.timers.keys()):
			print("warning! tried to get non-existent timer '{}'".format(name))
			n = type("nulltimer",(object,),{})()
			n.get = lambda: False
			return n
		return self.timers[name]

	def timeout(self,name):
		if not (name in self.timeouts.keys()):
			print("warning! tried to get non-existent timeout '{}'".format(name))
			n = type("nulltimeout",(object,),{})()
			n.get = lambda: False
			return n
		return self.timeouts[name][0]

	def being_addressed(self,line):
		text = line.rest
		direct = line.parameters[0] == self.nick
		match = any([n.lower() in line.rest.lower() for n in self.names])
		#self.mention_pattern = re.compile(r'((?:.*\b|^){0}(?:\b.*|$))'.format('|'.join(self.names)))
		#match = self.mention_pattern.match(text)
		if match or direct:
			return True
		return False

	def get_db(self,DBFILE='snuggles.sqlite'):
		if not os.path.exists(DBFILE):
			open(DBFILE,'w').close()
		self.db = sqlite3.connect(DBFILE)
		c = self.db.cursor()
		n = c.execute("SELECT count(*) FROM sqlite_master WHERE type='table';").fetchone()[0]
		if not (n > 1):
			print("sqlite db not set up! bailing")
			sys.exit()

	def flags(self,flagname,value=None):
		if value is None:
			return self._flags.get(flagname,False)
		elif value is True or value is False:
			self._flags[flagname] = value
		return None

	def flush_queue(self):
		while True:
			if not self.queue.empty():
				try:
					(out,wait) = self.queue.get_nowait()
				except queue.Empty:
					pass
				else:
					time.sleep(wait)
					self.transport.write(out)
					time.sleep(0.5)
			time.sleep(0.1)

	def console_input():
		while True:
			if not self.commandqueue.empty():
				try:
					c = self.commandqueue.get_nowait()
				except queue.Empty:
					pass
			self.process_command(c)
			time.sleep(0.1)

	def run(self):
		print("running thread for server!")
		self.thread = threading.Thread(target=self.flush_queue,daemon=True)
		self.thread.start()
		return #TODO delete
		print("running input thread!")
		self.consolethread = threading.Thread(target=self.console_input,daemon=True)
		self.consolethread.start()

	def get_alternate_nick(self,current):
		self.taken_nicks.append(current)
		new = randomly_replace_vowels(current)
		f = 0
		while new in self.taken_nicks:
			new = randomly_replace_vowels(current)
			f += 1
			if f > 10:
				new += random.choice(["_","`","-"])
			#TODO detect when we've exhausted the space???

	def check_expectations(self,line):
		expectations, self.expectations = self.expectations, []
		for expectation in expectations:
			e = expectation.check(line)
			if e is None:
				self.expectations.append(expectation)
			elif e is False:
				expectation.unwind()

class TickInterval:
	def __init__(self,interval,enabled):
		self.interval = interval
		self.enabled = enabled
