import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta


@module.type("PRIVMSG")
@module.disable
def echo_fn(bot,message,regex_matches=None):
	#bot.commands.privmsg(message.sender,"{}: you said '{}'".format(message.sender,message.message))
	if message.is_action:
		print("{}: you did '{}'".format(message.sender,message.message))
	else:
		print("{}: you said '{}'".format(message.sender,message.message))

echo = module.Module("echo")
echo.add_function(echo_fn)
