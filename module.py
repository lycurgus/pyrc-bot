import util
from functools import wraps
import re
import datetime

class Timeout:
	def __init__(self,name,days=0,hours=0,minutes=0,seconds=0):
		self.timeout = util.days(days) + util.hours(hours) + util.minutes(minutes) + seconds
		if self.timeout == 0:
			raise ValueError("Timeout '{}' is zero!".format(name))
		self.name = name
		self.mark = datetime.datetime.fromtimestamp(1)

	def get(self):
		expired = ((datetime.datetime.utcnow() - self.mark) > datetime.timedelta(seconds=self.timeout))
		if expired:
			self.mark = datetime.datetime.utcnow()
		return expired

class Timer:
	def __init__(self,name,days=0,hours=0,minutes=0,seconds=0):
		self.timer = util.days(days) + util.hours(hours) + util.minutes(minutes) + seconds
		if self.timer == 0:
			raise ValueError("Timer '{}' is zero!".format(name))
		self.name = name

class Module:
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
			bot.register_handler(function,self.name)
		for tfunction in self.timed_functions:
			bot.register_timed_function(tfunction,self.name)
		for timer in self.timers:
			bot.register_timer(timer,self.name)
		for timeout in self.timeouts:
			bot.register_timeout(timeout,self.name)
		if self.setup_function:
			self.setup_function(bot)

	def check_triggers(self,message,bot):
		matches = []
		for function in self.functions:
			#print('---------trigger check for {}'.format(function.__name__))
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
					#print("function {} has attribute {}: checking for match".format(getattr(function,"__name__"),a))
					if a == "direct":
						checks.append(bot.being_addressed(message.line))
						if any([message.message.startswith(bn.lower()) for bn in bot.names]):
							print('original message: {}'.format(message.original))
							message.message = re.sub(r'{}(?:[:, ])?'.format('|'.join(bot.names)),'',message.original,count=1,flags=re.IGNORECASE)
							print('altered message: {}'.format(message.message))
					elif a == "timeout":
						checks.append(bot.timeout(at).get())
					elif a == "type":
						checks.append(message.command in at)
					elif a == "sender":
						checks.append(message.sender in at)
					elif a == "sender-not":
						checks.append(message.sender not in at)
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
							checks.append(any([u.lower() in list(map(str.lower, bot.channels[message.channel].users.keys())) for u in at]))
						else:
							checks.append(False)
					elif a == "user-not-present":
						if message.channel:
							checks.append(all([u.lower() not in lower(bot.channels[message.channel].users.keys()) for u in at]))
						elif message.sender:
							if message.sender.lower() in lower(at):
								checks.append(False)
						else:
							checks.append(True)
					elif a == "mention":
						checks.append(any([bn in message.message for bn in bot.names]))
					elif a == "address":
						checks.append(any([any((message.message.startswith(bn),line.rest.endswith(bn))) for bn in bot.names]))
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
				if any(checks):
					matches.append((function,match))
			else:
				if all(checks):
					matches.append((function,match))
			return matches

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

def any(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	if hasattr(function,"all"):
		raise ModuleException("can't add @any to a function that already has @all")
	setattr(wrapper,"any",True)
	return wrapper

def all(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	if hasattr(function,"any"):
		raise ModuleException("can't add @all to a function that already has @any")
	setattr(wrapper,"all",True)
	return wrapper

def line(function):
	@wraps(function)
	def wrapper(*args,**kwargs):
		return function(*args,**kwargs)
	setattr(wrapper,"line",True)
	return wrapper

def command(commandname,requiredargs=0,optionalargs=0):
	def type_decorator(function):
		@wraps(function)
		def wrapper(*args,**kwargs):
			return function(*args,**kwargs)
		setattr(wrapper,"command",(commandname,requiredargs,optionalargs))
		return wrapper
	return type_decorator

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
