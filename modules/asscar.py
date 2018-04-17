import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta
import util

@module.type("PRIVMSG")
@module.regex(r".*\b([^\b]+)-ass (.+?)\b")
def ass_car(bot,message,regex_matches=None):
	if not bot.awake:
		return
	sweet = regex_matches.group(1)
	car = regex_matches.group(2)
	bot.commands.privmsg(message.replyto,"more like {} ass-{}, right?".format(sweet,car))

asscar = module.Module("asscar")
asscar.add_function(ass_car)
