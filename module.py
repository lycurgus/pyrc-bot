import util
from functools import wraps
import re
import datetime



def check_function(function,message,bot):
	match = None
	if not message.message:
		return (False,None)
	check_attributes = list(set(Module.triggers).intersection(dir(function)))
	if "direct" in check_attributes:
		check_attributes.remove("direct")
		check_attributes.insert(0,"direct")
	if "disable" in check_attributes:
		check_attributes.remove("disable")
		check_attributes.insert(0,"disable")
	for a in check_attributes:
		if hasattr(function,a):
			at = getattr(function,a,None)
			if a == "direct":
				if any([message.message.startswith(bn.lower()) for bn in bot.names]):
					print('original message: {}'.format(message.original))
					message.message = re.sub(r'{}(?:[:, ])?'.format('|'.join(bot.names)),'',message.original,count=1,flags=re.IGNORECASE)
					print('altered message: {}'.format(message.message))
				if not bot.being_addressed(message.line): return (False,None)
			elif a == "disable":
				return (False,None)
			elif a == "timeout":
				expired = bot.timeout(at).get()
				if not expired: return (False,None)
				bot.timeout(at).set()
			elif a == "type":
				if not message.command in at: return (False,None)
			elif a == "sender":
				if not message.sender: return (False,None)
				if not message.sender.lower() in util.lower(at): return (False,None)
			elif a == "sender-not":
				if message.sender:
					if message.sender.lower() in util.lower(at): return (False,None)
			elif a == "sender-admin":
				if not bot.is_admin(message.sender): return (False,None)
			elif a == "sender-not-admin":
				if bot.is_admin(message.sender): return (False,None)
			elif a == "channel":
				if not message.channel in at: return (False,None)
			elif a == "channel-not":
				if message.channel in at: return (False,None)
			elif a == "user-present":
				if not message.channel: return (False,None)
				if not any([u.lower() in util.lower(bot.channels[message.channel].users.keys()) for u in at]): return (False,None)
			elif a == "user-not-present":
				if message.sender:
					if message.sender.lower() in util.lower(at): return (False,None)
				if message.channel:
					if any([u.lower() in util.lower(bot.channels[message.channel].users.keys()) for u in at]): return (False,None)
			elif a == "mention":
				if not any([bn in message.message for bn in bot.names]): return (False,None)
			elif a == "address":
				if not any([any((message.message.startswith(bn),line.rest.endswith(bn))) for bn in bot.names])): return (False,None)
			elif a == "action":
				if not message.is_ctcp: return (False,None)
				if not message.original.upper().startswith("ACTION"): return (False,None)
				message.message = re.sub(r'^ACTION ','',message.original,count=1)
			elif a == "ctcp":
				if not message.is_ctcp: return (False,None)
			elif a == "regex":
				match = at.match(message.message)
				if not match: return (False,None)
	return (True,match)




class Timeout:
	def __init__(self,name,days=0,hours=0,minutes=0,seconds=0):
		self.timeout = util.days(days) + util.hours(hours) + util.minutes(minutes) + seconds
		if self.timeout == 0:
			raise ValueError("Timeout '{}' is zero!".format(name))
		self.name = name
		self.mark = datetime.datetime.fromtimestamp(1)

	def get(self):
		expired = ((datetime.datetime.utcnow() - self.mark) > datetime.timedelta(seconds=self.timeout))
		return expired

	def set(self):
		self.mark = datetime.datetime.utcnow()

class Timer:
	def __init__(self,name,days=0,hours=0,minutes=0,seconds=0):
		self.timer = util.days(days) + util.hours(hours) + util.minutes(minutes) + seconds
		if self.timer == 0:
			raise ValueError("Timer '{}' is zero!".format(name))
		self.name = name

class Module:
	triggers = [
			"timeout",
			"type",
			"sender",
			"sender-not",
			"sender-admin",
			"sender-not-admin",
			"channel",
			"channel-not",
			"user-not-present",
			"mention",
			"address",
			"direct",
			"regex",
			"action",
			"ctcp",
			"disable"
		]
	def __init__(self,name):
		self.functions = []
		self.timed_functions = []
		self.timers = []
		self.timeouts = []
		self.name = name
		self.setup_function = None

	def add_function(self,function):
		if not hasattr(function,"type"):
			setattr(function,"type",["PRIVMSG"])
		if not hasattr(function,"line"):
			setattr(function,"message",True)
		if hasattr(function,"timer"):
			self.timed_functions.append(function)
		else:
			self.functions.append(function)

	def add_timer(self,name,days=0,hours=0,minutes=0,seconds=0):
		t = Timer(name,days,hours,minutes,seconds)
		self.timers.append(t)

	def add_timeout(self,name,days=0,hours=0,minutes=0,seconds=0):
		t = Timeout(name,days,hours,minutes,seconds)
		self.timeouts.append(t)

	def initialise(self,bot):
		for function in self.functions:
			if hasattr(function,"regex"):
				r = getattr(function,"regex")
				if "_BOTNAMES_" in r.pattern:
					newpattern = re.sub(r"_BOTNAMES_","(?:{})".format("|".join(bot.names)))
					setattr(function,"regex",re.compile(newpattern,r.flags))
		for tfunction in self.timed_functions:
			bot.register_timed_function(tfunction,self.name)
		for timer in self.timers:
			bot.register_timer(timer,self.name)
		for timeout in self.timeouts:
			bot.register_timeout(timeout,self.name)
		if self.setup_function:
			self.setup_function(bot)

	def check_triggers(self,message,bot):
		timeout = ""
		matches = []
		for function in self.functions:
			checks = []
			checknames = []
			match = None
			if not message.message:
				return ()
			#print("function {} has attributes {}".format(function.__name__," ".join([attrib for attrib in dir(function) if not attrib.startswith("__")])))
			check_attributes = list(set(Module.triggers).intersection(dir(function)))
			if "direct" in check_attributes:
				check_attributes.remove("direct")
				check_attributes.insert(0,"direct")
			for a in check_attributes:
				if hasattr(function,a):
					checknames.append(a)
					at = getattr(function,a,None)
					if a == "direct":
						checks.append(bot.being_addressed(message.line))
						if any([message.message.startswith(bn.lower()) for bn in bot.names]):
							print('original message: {}'.format(message.original))
							message.message = re.sub(r'{}(?:[:, ])?'.format('|'.join(bot.names)),'',message.original,count=1,flags=re.IGNORECASE)
							print('altered message: {}'.format(message.message))
					elif a == "timeout":
						timeout = at
						expired = bot.timeout(at).get()
						checks.append(expired)
					elif a == "type":
						checks.append(message.command in at)
					elif a == "sender":
						if message.sender:
							checks.append(message.sender.lower() in util.lower(at))
						else:
							checks.append(False)
					elif a == "sender-not":
						if message.sender:
							checks.append(message.sender.lower() not in util.lower(at))
						else:
							checks.append(True)
					elif a == "sender-admin":
						checks.append(bot.is_admin(message.sender))
					elif a == "sender-not-admin":
						checks.append(not bot.is_admin(message.sender))
					elif a == "channel":
						checks.append(message.channel in at)
					elif a == "channel-not":
						checks.append(message.channel not in at)
					elif a == "user-present":
						if message.channel:
							checks.append(any([u.lower() in util.lower(bot.channels[message.channel].users.keys()) for u in at]))
						else:
							checks.append(False)
					elif a == "user-not-present":
						if message.channel:
							present = []
							for u in at:
								user_found = False
								for cu in bot.channels[message.channel].users.keys():
									if cu.lower() == u.lower():
										user_found = True
								present.append(user_found)
							checks.append(not any(present))
						elif message.sender:
							if message.sender.lower() in util.lower(at):
								checks.append(False)
						else:
							checks.append(True)
					elif a == "mention":
						checks.append(any([bn in message.message for bn in bot.names]))
					elif a == "address":
						checks.append(any([any((message.message.startswith(bn),line.rest.endswith(bn))) for bn in bot.names]))
					elif a == "action":
						#print("action original: {}".format(repr(message.original)))
						#action = re.match(r"^\x01(.*)\x01$",message.original)
						action = message.is_ctcp and message.original.upper().startswith("ACTION")
						if action:
							checks.append(True)
							message.message = re.sub(r'^ACTION ','',message.original,count=1)
						else:
							checks.append(False)
					elif a == "ctcp":
						checks.append(True if message.is_ctcp else False)
					elif a == "regex":
						match = at.match(message.message)
						checks.append(True if match else False)
					elif a == "disable":
						checks.append(False)
			if all(checks):
				if timeout != "":
					if bot.timeout(timeout).get():
						bot.timeout(timeout).set() #TODO: check functions individually so this can be kept in the body of the check??
				matches.append((function,match))
		return matches



	def check_timers(self,bot,tick_num,delta):
		for timer in self.timers:
			if (tick_num % int(round(timer.timer/delta)) == 0):
				for function in self.timed_functions:
					if getattr(function,"timer",None) == timer.name:
						function(bot,None,None)

def ModuleException(Exception): pass

def timeout(name):
	def timeout_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"timeout",name)
		return wrapper
	return timeout_decorator

def timer(name):
	def timer_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"timer",name)
		return wrapper
	return timer_decorator

def type(types):
	def type_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"type",util.listify(types))
		return wrapper
	return type_decorator

def line(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"line",True)
	return wrapper

def admin(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"sender-admin",True)
	return wrapper

def not_admin(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"sender-not-admin",True)
	return wrapper

def sender(senders):
	def sender_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"sender",util.listify(senders))
		return wrapper
	return sender_decorator

def sender_not(senders):
	def sender_not_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"sender-not",util.listify(senders))
		return wrapper
	return sender_not_decorator

def channel(channels):
	def channel_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"channel",util.listify(channels))
		return wrapper
	return channel_decorator

def channel_not(channels):
	def channel_not_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"channel-not",util.listify(channels))
		return wrapper
	return channel_not_decorator

def regex(regex,flags=re.IGNORECASE):
	def regex_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"regex",re.compile(regex,flags))
		return wrapper
	return regex_decorator

def ctcp(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"ctcp",True)
	return wrapper

def action(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"action",True)
	return wrapper

def mention(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"mention",True)
	return wrapper

def address(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"address",True)
	return wrapper

def direct(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"direct",True)
	return wrapper

def disable(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"disable",True)
	return wrapper

def user_present(users):
	def user_present_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"user-present",util.listify(users))
		return wrapper
	return user_present_decorator

def user_not_present(users):
	def user_not_present_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"user-not-present",util.listify(users))
		return wrapper
	return user_not_present_decorator
