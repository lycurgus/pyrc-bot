import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import re
from datetime import timedelta
from util import Expectation

jimmy_nicks = ["jimmy","jimmy42","cha0zzb0t","blob","sleepybalrog","hungrybalrog","redhotbalrog","uberjimmy","redhotjimmy"]

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.command("!bed")
def gotobed(bot,message,regex_matches=None):
	if not bot.awake:
		bot.commands.action(message.replyto,"is already in bed")
		return
	bot.commands.action(message.replyto,"puts on a scary mask")
	bot.commands.action(message.replyto,"yells at a pillow")
	bot.commands.action(message.replyto,"takes off the scary mask")

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.command("!work")
def backtowork(bot,message,regex_matches=None):
	if not bot.awake:
		bot.commands.action(message.replyto,"is too sleepy to work")
		return
	bot.commands.action(message.replyto,"puts on a scary mask")
	bot.commands.action(message.replyto,"yells at {}".format(message.sender))
	bot.commands.action(message.replyto,"takes off the scary mask")

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^!time (.*)$")
#@module.command("!time",1)
def timecheck(bot,message,regex_matches=None):
	#target = message.line.rest.split(" ",1)[1].lower() #TODO get target from command regex
	target = regex_matches.group(1)
	if target.lower() == bot.nick.lower():
		bot.commands.privmsg(message.replyto,"time to get a watch! hahahaha")
		return
	c = {
			'nick': target,
			'type': 'NOTICE',
			'regex': re.compile(r"^\x01TIME .*\x01$")
		}
	a = [bot.commands.privmsg]
	p = [[message.replyto,[re.compile(r'^\x01TIME (.*)\x01$'),1],True]]
	e = timedelta(minutes=1)
	bot.expectations.append(Expectation(c,a,p,e))
	bot.commands.ctcp_ask(target,"TIME")

@module.user_not_present(jimmy_nicks)
@module.type("PRIVMSG")
@module.regex(r"^!no+$")
def noooo(bot,message,regex_matches=None):
	if not bot.awake:
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
