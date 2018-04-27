import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from datetime import timedelta
import util

@module.type("PRIVMSG")
@module.regex(r".*\b([^\b]+)-ass (.+?)\b")
def ass_car(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		return
	sweet = regex_matches.group(1)
	car = regex_matches.group(2)
	bot.commands.privmsg(message.replyto,"more like {} ass-{}, right?".format(sweet,car))

asscar = module.Module("asscar")
asscar.add_function(ass_car)
