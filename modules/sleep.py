import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util
from datetime import datetime
import time
import math

def get_t(offset,waketime,bedtime):
	t = ((time.time() + offset) % 86400) / 60 #minutes - 1440 to a day
	today = datetime.today().weekday()
	wake = waketime * 60
	sleep = bedtime * 60
	if today in (4,5):#friday or saturday
		sleep += 60
	if today in (5,6):#saturday or sunday
		wake += 60
	#c = 1 - (0.5*(math.tanh(0.1*(t-wake)) + math.tanh(-0.1*(t-sleep)))) #p(asleep)
	c = 0.5*(math.tanh(0.1*(t-wake)) + math.tanh(-0.1*(t-sleep))) #p(awake)
	#return 1 - c
	return c

def initial_set(bot):
	print('setting initial sleep state!')
	s = not util.chance(get_t(bot.gmtoffset,bot.waketime,bot.bedtime))
	bot.setcustom('asleep',s)

def unload(bot):
	bot.removecustom('asleep')

@module.timer("wakecheck")
def check_awake(bot,line,regex_matches=None):
	if not bot.timeout('justwokeorslept').get():
		return
	t = get_t(bot.gmtoffset,bot.waketime,bot.bedtime)
	old_wake = not bot.getcustom('asleep')
	print('checking wake state!')
	new_wake = util.chance(t)
	bot.setcustom('asleep',not new_wake)
	if new_wake != old_wake:
		if new_wake:
			bot.commands.unaway(bot.nick)
			for channel in bot.channels:
				bot.commands.action(channel,"yawns and stretches")
				bot.commands.privmsg(channel,"good morning :)")
		else:
			bot.commands.away("having an adorable nap")
			for channel in bot.channels:
				bot.commands.action(channel,"yawns")
				bot.commands.privmsg(channel,"time to sleep, good night!")

@module.admin
@module.timeout("nap")
@module.command("have a nap")
def nap(bot,message,regex_matches=None):
	print('nap requested. asleep: {}'.format(bot.getcustom('asleep')))
	if bot.getcustom('asleep'):
		return None
	bot.setcustom('asleep',True)
	bot.commands.privmsg(message.replyto,"good idea :)")
	bot.commands.action(message.replyto,"settles down for a nap")
	def nap_wake():
		bot.setcustom('asleep',False)
		bot.commands.action(message.replyto,"wakes from her nap")
	bot.queue_action(minutes(10),nap_wake)

@module.admin
@module.timeout("nap")
@module.command("wake up")
def short_wake(bot,message,regex_matches=None):
	if not bot.getcustom('asleep'):
		return None
	bot.setcustom('asleep',False)
	bot.commands.action(message.replyto,"stirs and wakes")
	bot.commands.privmsg(message.replyto,"what's up? i was sleeping...")
	def back_to_bed():
		bot.setcustom('asleep',True)
		bot.commands.action(message.replyto,"goes back to bed")
	bot.queue_action(minutes(10),back_to_bed)

@module.admin
@module.action
@module.regex(r"pokes (.*)")
def get_poked(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if bot.getcustom('asleep'):
		print("poked while asleep")
	else:
		print("poked while awake")
	check_awake(bot,message,regex_matches)

@module.direct
@module.regex(r"are you awake?")
def are_you_awake(bot,message,regex_matches=None):
	if not bot.getcustom('asleep'):
		bot.commands.privmsg(message.replyto,"yep :)")
	elif util.chance(0.5):
		bot.commands.action(message.replyto,"snores")
	print("{} ({})".format(str(not bot.getcustom('asleep')),get_t(bot.gmtoffset,bot.waketime,bot.bedtime)))

sleep = module.Module("sleep")
sleep.add_function(nap)
sleep.add_function(short_wake)
sleep.add_timer("wakecheck",minutes=10)
sleep.add_function(check_awake)
sleep.add_timeout("justwokeorslept",minutes=20)
sleep.add_timeout("nap",minutes=10)
sleep.add_function(get_poked)
sleep.add_function(are_you_awake)
sleep.setup_function = initial_set
