import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util

@module.regex(r"(?:maximum )?rabbit")
@module.type("PRIVMSG")
def max_rabbit(bot,message,regex_matches=None):
	if util.chance(0.9):
		return
	bot.commands.privmsg(message.replyto,"ᴍᴀxɪᴍᴜᴍ ʀᴀʙʙɪᴛ")

maximum = module.Module("maximum")
maximum.add_function(max_rabbit)
