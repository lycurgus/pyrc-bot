import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta
import util

@module.type("PRIVMSG")
@module.regex(r"\(╯°□°）╯︵ ?┻━┻")
def respecttables(bot,message,regex_matches=None):
	if util.chance(0.9):
		return
	bot.commands.privmsg(message.replyto,"┬┬ ノ(゜-゜ノ)")

pleaserespecttables = module.Module("pleaserespecttables")
pleaserespecttables.add_function(respecttables)
