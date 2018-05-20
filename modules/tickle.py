import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random
import util

@module.type("PRIVMSG")
@module.action
@module.regex(r"tickles _BOTNAMES_.*")
def tickle_respond(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		response = random.choice(["giggles","smiles and giggles"])
	else:
		response = random.choice(["squirms in her sleep"])
	bot.commands.action(message.replyto,response)

tickle = module.Module("tickle")
tickle.add_function(tickle_respond)
