import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from datetime import timedelta
import util

#TODO bring the other style of match into this file (currently in gift.py)

@module.type("PRIVMSG")
@module.action
@module.regex(r"gives (.*)(?:a )?hugs?")
def givehug(bot,message,regex_matches=None):
	if regex_matches.group(1).lower() in util.lower(bot.names):
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"hugs {} back".format(message.sender))
		else:
			bot.commands.action(message.replyto,"sleepily hugs {} back".format(message.sender))

@module.action
@module.regex(r"hugs (.*)")
def hugs(bot,message,regex_matches=None):
	hugee = regex_matches.group(1).split(" ")[0]
	print("hugee was {}".format(hugee))
	if hugee.lower() in util.lower(bot.names):
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"hugs {} back".format(message.sender))
		else:
			bot.commands.action(message.replyto,"sleepily hugs {} back".format(message.sender))
	else:
		if util.chance(0.1) and not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"joins in the hug with {hugger} and {huggee}".format(hugger=message.sender,huggee=hugee))

@module.type("PRIVMSG")
@module.action
@module.regex(r"gives (.*)(?:a )?snuggles?")
def givesnuggle(bot,message,regex_matches=None):
	if regex_matches.group(1).lower() in util.lower(bot.names):
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"snuggles {} back".format(message.sender))
		else:
			bot.commands.action(message.replyto,"sleepily snuggles {}".format(message.sender))

@module.type("PRIVMSG")
@module.action
@module.regex(r"snuggles (.*)")
def snuggle(bot,message,regex_matches=None):
	hugee = regex_matches.group(1).split(" ")[0]
	if hugee.lower() in util.lower(bot.names):
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"snuggles {} back".format(message.sender))
		else:
			bot.commands.action(message.replyto,"sleepily snuggles {}".format(message.sender))

hug = module.Module("hug")
hug.add_function(hugs)
hug.add_function(givehug)
hug.add_function(snuggle)
hug.add_function(givesnuggle)
