import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import os
import module

@module.regex(r".*break a fortune cookie.*")
@module.user_not_present(["taiya","mechataiya","narwhaltaiya"])
@module.type("PRIVMSG")
def fortune_cookie(bot,message,regex_matches=None):
	fortune = os.popen('fortune -s').read()
	bot.commands.privmsg(message.replyto,"the fortune cookie says: {}".format(fortune),True)

fortune = module.Module("fortune")
fortune.add_function(fortune_cookie)
