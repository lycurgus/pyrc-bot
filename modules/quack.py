import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util

@module.timeout("quack")
@module.type("PRIVMSG")
@module.regex(r"\bquack\b")
def react_duck(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		if util.chance(0.3):
			bot.commands.privmsg(message.replyto,"a duck!")
			bot.commands.action(message.replyto,"pounces on the ducky")
	else:
		if util.chance(0.15):
			bot.commands.action(message.replyto,"quacks sleepily")

quack = module.Module("quack")
quack.add_function(react_duck)
quack.add_timeout("quack",seconds=20)
