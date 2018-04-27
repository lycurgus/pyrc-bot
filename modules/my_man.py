import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random
import util

@module.regex(r"my man!|slow down!|lookin' good!")
@module.type("PRIVMSG")
def myman(bot,message,regex_matches=None):
	if util.chance(0.95):
		return
	response = random.choice([
		"my man!",
		"*snap* Yes!",
		"slow down!",
		"lookin' good!"
	])
	bot.commands.privmsg(message.replyto,response)

my_man = module.Module("my_man")
my_man.add_function(myman)
