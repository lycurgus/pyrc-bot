import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from colours import replace

@module.type("PRIVMSG")
@module.regex(r"^echo (.*)")
def echo_fn(bot,message,regex_matches=None):
	e = regex_matches.group(1)
	e = replace(e)
	bot.commands.privmsg(message.sender,e)

echo = module.Module("echo")
echo.add_function(echo_fn)
