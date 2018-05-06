import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util

@module.regex("^dolphin noises$")
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
