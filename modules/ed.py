import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

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
