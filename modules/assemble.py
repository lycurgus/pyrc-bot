import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util
import re
import random

@module.type("PRIVMSG")
@module.regex(r"^\s*bots,?\s+assemble\s*!\s*$")
@module.timeout("assemble")
def bots_assemble(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		resp = random.choice([
			"the almighty fluffiest",
			"longest ears in the West",
			"queen of the carrots",
			"professional hugger"
		])
		bot.commands.privmsg(message.replyto,"SnuggleBunny, {}!".format(resp))
	else:
		bot.commands.action(message.replyto,"strikes a pose in her sleep")

@module.type("PRIVMSG")
@module.regex(r"^\s*bots,?\s+assemble\s*$")
@module.timeout("assemble")
def bots_assemble_i_guess(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		if util.chance(0.5):
			bot.commands.action(message.replyto,"half-assedly strikes a pose")
		else:
			bot.commands.privmsg(message.replyto,"yeah i'm here")
	else:
		if util.chance(0.4):
			bot.commands.action(message.replyto,"snores")

assemble = module.Module("assemble")
assemble.add_function(bots_assemble)
assemble.add_function(bots_assemble_i_guess)
assemble.add_timeout("assemble",seconds=30)

#	elif line.rest.lower() in ["bots, roll call","bots: roll call","who here is a bot?","who are the bots?","who here is a bot","who are the bots"]:
#		if not bot.getcustom("asleep"):
#			bot.commands.action(replyto,"raises a paw")
#			bot.commands.privmsg(replyto,":)")
#		else:
#			bot.commands.action(replyto,"raises a paw sleepily")
