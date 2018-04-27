import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import ed

@module.disable
@module.regex(r"ed(?: (.*))?")
@module.type("PRIVMSG")
def ed_set(bot,message,regex_matches=None):
	fn = regex_matches.group(1)
	if not hasattr(bot,"ed"):
		bot.ed = ed.Ed(filename=fn)
	bot.ed.start(message.sender)

ed = module.Module("ed")
ed.add_function(ed_set)
