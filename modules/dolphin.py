import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util

@module.command("dolphin noises")
@module.timeout("dolphins")
@module.type("PRIVMSG")
def dolphin_func(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,"oh, a dolphin")
		if util.chance(0.98):
			bot.commands.action(message.replyto,"whistles and clicks")
		else:
			bot.commands.action(message.replyto,"raep")
	else:
		if util.chance(0.4):
			bot.commands.action(message.replyto,"whistles in her sleep")

dolphin = module.Module("dolphin")
dolphin.add_function(dolphin_func)
dolphin.add_timeout("dolphins",seconds=2)
