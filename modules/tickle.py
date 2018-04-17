import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import random
import util

@module.type("PRIVMSG")
@module.action
@module.regex(r"tickles ([^\s]*).*")
def tickle_respond(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if bot.awake:
		response = random.choice(["is tickled"])
	else:
		response = random.choice(["is tickled while asleep"])
	bot.commands.action(message.replyto,response)

tickle = module.Module("tickle")
tickle.add_function(tickle_respond)
