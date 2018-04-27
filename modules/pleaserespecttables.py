import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

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
