import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta
import util

#@module.timeout(timedelta(hours=1),"echo")
@module.type("PRIVMSG")
@module.regex(r"\band shit\b")
@module.user_not_present(["quackthing"])
def and_shit(bot,message,regex_matches=None):
	if not bot.awake:
		return
	if util.chance(0.1):
		bot.commands.privmsg(message.replyto,"and shit???")

andshit = module.Module("andshit")
andshit.add_function(and_shit)
