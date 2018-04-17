import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util
from datetime import datetime
import time
import math

#TODO invert the sense of all these and change the name to "asleep" - so that other modules will get a reasonable "False" or "None" if they try to get the property
#TODO so switch all checks of if bot.awake to if not bot.getcustom('asleep')

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
	s = util.chance(get_t(bot.gmtoffset,bot.waketime,bot.bedtime))
	bot.awake = s
	bot.setcustom('asleep',s)

def unload(bot):
	bot.removecustom('asleep')

@module.timer("wakecheck")
def check_awake(bot,line,regex_matches=None):
	if not bot.timeout('justwokeorslept').get():
		return
	t = get_t(bot.gmtoffset,bot.waketime,bot.bedtime)
	old_wake = bot.getcustom('asleep')
	old_wake = bot.awake
	print('checking wake state!')
	bot.awake = util.chance(t)
	bot.setcustom('asleep',bot.awake)
	if bot.awake != old_wake:
		if bot.awake:
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
	print('nap requested. awake: {}'.format(bot.awake))
	if not bot.awake:
		return None
	bot.awake = False
	bot.commands.privmsg(message.replyto,"good idea :)")
	bot.commands.action(message.replyto,"settles down for a nap")
	def nap_wake():
		bot.awake = True
		bot.commands.action(message.replyto,"wakes from her nap")
	bot.queue_action(minutes(10),nap_wake)

@module.admin
@module.timeout("nap")
@module.command("wake up")
def short_wake(bot,message,regex_matches=None):
	if bot.awake:
		return None
	bot.awake = True
	bot.commands.action(message.replyto,"stirs and wakes")
	bot.commands.privmsg(message.replyto,"what's up? i was sleeping...")
	def back_to_bed():
		bot.awake = False
		bot.commands.action(message.replyto,"goes back to bed")
	bot.queue_action(minutes(10),back_to_bed)

@module.admin
@module.action
@module.regex(r"pokes (.*)")
def get_poked(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if bot.awake:
		print("poked while awake")
	else:
		print("poked while asleep")
	check_awake(bot,message,regex_matches)

@module.direct
@module.regex(r"are you awake?")
def are_you_awake(bot,message,regex_matches=None):
	if bot.awake:
		bot.commands.privmsg(message.replyto,"yep :)")
	elif util.chance(0.5):
		bot.commands.action(message.replyto,"snores")
	print("{} ({})".format(str(bot.awake),bot.get_t(bot.gmtoffset)))

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
