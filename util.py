#!/usr/bin/env python3

from blinker import signal
import datetime
import re
import random
from time import sleep

class Regexes:
	ctcp = re.compile(r'^\x01(.*)(?: (.*))?\x01$')

class Expectation:
	re_type = type(re.compile(r'hello, world'))
	def __init__(self,c,a,p,e,ea=[],ep=[[]]):
		self.conditions = c#{}
		self.actions = a#[]
		self.parameters = p#[[]]
		self.expiry = datetime.datetime.now() + e#timedelta
		self.expiry_actions = ea#[]
		self.expiry_parameters = ep#[[]]

	def check(self,message):
		if datetime.datetime.now() > self.expiry:
			return False
		if self.conditions.get('regex',None): #regex match
			m = re.match(self.conditions['regex'],message.message)
			if not m:
				return None
		if self.conditions.get('type',None): #message type
			if not message.command == self.conditions['type']:
				return None
		if self.conditions.get('or',None): #message contains any of the terms
			ors = self.conditions['or']
			if not any([t in message.message for t in ors]):
				return None
		if self.conditions.get('and',None): #message contains all of the terms
			ands = self.conditions['and']
			if not all([t in message.message for t in ands]):
				return None
		if self.conditions.get('not',None): #message contains none of the terms
			nots = self.conditions['not']
			if any([t in message.message for t in nots]):
				return None
		if self.conditions.get('nick',None): #message came from given user
			if not message.nick.lower() == self.conditions['nick'].lower():
				return None
		#if we made it here, none of our set conditions failed and we weren't expired
		#print("initial parameters: {}".format(self.parameters))
		for j,pset in enumerate(self.parameters):
			for k,p in enumerate(pset):
				if isinstance(p,list):
					if type(p[0]) == Expectation.re_type:
						self.parameters[j][k] = p[0].match(line.rest).group(p[1])
		for i,action in enumerate(self.actions):
			action(*self.parameters[i])
		return True

	def unwind(self):
		for i,action in enumerate(self.expiry_actions):
			action(*self.expiry_parameters[i])

def listify(candidate):
	if not isinstance(candidate,list):
		candidate = [candidate]
	return candidate

def lower(l):
	if isinstance(l,type({}.keys())):
		l = [*l]
	return list(map(str.lower,list(map(str,listify(l)))))

def weeks(w):
	return days(7) * w

def days(d):
	return 86400 * d#hours(24) * d

def hours(h):
	return 3600 * h#minutes(60) * h

def minutes(m):
	return 60 * m

def randomly_replace_vowels(word,count=None):
	import random
	c = count
	vowels = ["a","e","i","o","u"]
	if not any([v in word.lower() for v in vowels]):
		return word
	for index,letter in enumerate(word):
		if letter in vowels:
			word[index] = random.choice([v for v in vowels if v != letter.lower()])
			if letter.isupper():
				word[index] = word[index].upper()
			if c:
				c += 1
				if c >= count:
					break
	return word

def random_characters(n):
	import random
	import string
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def get_indefinite(word):
	if word[:1].lower() in ["a","e","i","o","u"]: #:1 accounts for zero-length string
		return "an"
	else:
		return "a"

class User:
	def __init__(self):
		self.last_talked = 0
		self.last_line = ""
		self.channels = []

	def talked(self,text):
		self.last_talked = datetime.datetime.utcnow()
		self.last_line = text

class Pronouns:
	def __init__(self,nom="they",acc="them",gen="their",pos="theirs"):
		self.nominative = nom
		self.accusative = acc
		self.genitive = gen
		self.possessive = pos

class Timer:
	def __init__(self):
		self.timeout = 1
		self.mark = datetime.datetime.fromtimestamp(1)

	def get(self):
		return ((datetime.datetime.utcnow() - self.mark) > datetime.timedelta(seconds=self.timeout))

	def set(self):
		self.mark = datetime.datetime.utcnow()

	def set_timeout(self,timeout):
		self.timeout = timeout

class Channel:
	def __init__(self,name):
		self.last_line = ""
		self.last_line_time = 0
		self.activityindex = 0
		self.topic = ""
		self.users = {}
		self.timers = {}
		self.modes = set()
		self.name = name
		sig_tick = signal("TICK-base")
		def dec_chanact(sender,**kwargs):
			self.decrement_activity()
		self.dec_chanact = dec_chanact
		sig_tick.connect(dec_chanact)

	def timer(self,name):
		if not (name in self.timers.keys()):
			self.timers[name] = Timer()
		return self.timers[name]

	def add_user(self,username):
		self.users[username] = User()
		self.users[username].channels.append(self.name)

	def remove_user(self,username):
		if username in self.users.keys():
			del self.users[username]

	def rename_user(self,oldnick,newnick):
		if oldnick in self.users.keys():
			self.users[newnick] = self.users[oldnick]
			del self.users[oldnick]

	def line_seen(self):
		self.activityindex += 10
		if self.activityindex > 50:
			self.activityindex = 50

	def decrement_activity(self):
		if not self.activityindex < 0:
			self.activityindex -= 0.1
			if self.activityindex < 0:
				self.activityindex = 0
		#print('channel activity for {} is {}'.format(self.name,self.activityindex))

class NickStatus:
	def __init__(self,active):
		self.active = active
		self.time = datetime.datetime.now()

def input_prefill(prompt,text):
	def hook():
		readline.insert_text(text)
		readline.redisplay()
	readline.set_pre_input_hook(hook)
	result = input(prompt)
	readline.set_pre_input_hook()
	return result

def chance(value=0):
	if value > 1:
		print('err! chance() takes a value between 0 and 1')
		value = 0
	return (random.random() < value)

def find_on_server(bot,nick):
	bot.commands.whois(nick) #issue a WHOIS request
	sleep(10) #wait a bit to let a response come in - can we yield or similar and get awoken when one comes..?
	if nick in bot.seen_users.keys():
		return bot.seen_users[nick].active
	return False #if no reply from the server in time assume they were absent

def tick():
	return "✓"

def cross():
	return "✘"

if __name__ == "__main__":
	from time import sleep
	while True:
		print(discord_time())
		sleep(1)
