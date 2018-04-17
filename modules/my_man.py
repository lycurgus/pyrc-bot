import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

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
