import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import re
from datetime import timedelta, datetime
import util

jimmy_nicks = ["jimmy","jimmy42","cha0zzb0t","blob","sleepybalrog","hungrybalrog","redhotbalrog","uberjimmy","redhotjimmy"]

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^\!bed$")
def gotobed(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		bot.commands.action(message.replyto,"is already in bed")
		return
	bot.commands.action(message.replyto,"puts on a scary mask")
	bot.commands.action(message.replyto,"yells at a pillow")
	bot.commands.action(message.replyto,"takes off the scary mask")

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^\!work$")
def backtowork(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		bot.commands.action(message.replyto,"is too sleepy to work")
		return
	bot.commands.action(message.replyto,"puts on a scary mask")
	bot.commands.action(message.replyto,"yells at {}".format(message.sender))
	bot.commands.action(message.replyto,"takes off the scary mask")

def time_string():
	partial = ""
	numbers = ["one","two","three","four","five","six","seven","eight","nine","ten","eleven"]
	hours = ["midnight"] + numbers + ["noon"] + numbers + ["midnight"]
	time = datetime.now()
	hr = time.hour
	mn = time.minute
	if mn < 10: partial = "just after"
	elif mn < 20: partial = "a quarter past"
	elif mn < 40: partial = "half past"
	elif mn < 50:
		partial = "a quarter to"
		hr += 1
	else:
		partial = "almost"
		hr += 1
	if hr < 12: day = "in the morning"
	elif hr < 13: day = ""
	elif hr < 18: day = "in the afternoon"
	elif hr < 20: day = "in the evening"
	elif hr < 24: day = "at night"
	else: day = ""
	return "it's {} {} {}".format(partial,hours[hr],day)

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^!time (.*)$")
def timecheck(bot,message,regex_matches=None):
	target = regex_matches.group(1)
	if target.lower() == bot.nick.lower():
		if not bot.getcustom("asleep"):
			if util.chance(0.3):
				bot.commands.privmsg(message.replyto,"time to get a watch! hahahaha")
			else:
				bot.commands.privmsg(message.replyto,time_string())
		else:
			bot.commands.action(message.replyto,"snores")
		return
	c = {
			'nick': target,
			'type': 'NOTICE',
			'regex': re.compile(r"^TIME (?!\s*(?:gb|goat(?:bot)?) ).*$")
		}
	a = [bot.commands.privmsg]
	p = [[message.replyto,[re.compile(r'^TIME (.*)$'),1],True]]
	e = timedelta(seconds=15)
	bot.expectations.append(util.Expectation(bot,c,a,p,e))
	bot.commands.ctcp_ask(target,"TIME")

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^!no+$")
def noooo(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		bot.commands.action(message.replyto,"is too sleepy to be upset")
		return
	bot.commands.action(message.replyto,"falls to her knees")
	if message.channel:
		if "sky" in list(map(str.lower,bot.channels[message.channel].users.keys())):
			bot.commands.action(message.replyto,"yells upward")
		else:
			bot.commands.action(message.replyto,"yells at the sky")
	else:
		bot.commands.action(message.replyto,"yells at the sky")

jimmy = module.Module("jimmy")
jimmy.add_function(gotobed)
jimmy.add_function(backtowork)
jimmy.add_function(timecheck)
jimmy.add_function(noooo)

#✓ ✘
