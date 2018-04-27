import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random
import util

@module.type("PRIVMSG")
@module.action
@module.regex(r"tickles ([^\s]*).*")
def tickle_respond(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if not bot.getcustom("asleep"):
		response = random.choice(["is tickled"])
	else:
		response = random.choice(["is tickled while asleep"])
	bot.commands.action(message.replyto,response)

tickle = module.Module("tickle")
tickle.add_function(tickle_respond)
