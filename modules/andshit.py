import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from datetime import timedelta
import util

@module.type("PRIVMSG")
@module.regex(r"\band shit\b")
@module.user_not_present(["quackthing"])
def and_shit(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		return
	if util.chance(0.1):
		bot.commands.privmsg(message.replyto,"and shit???")

andshit = module.Module("andshit")
andshit.add_function(and_shit)
