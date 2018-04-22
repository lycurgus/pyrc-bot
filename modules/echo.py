import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

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
