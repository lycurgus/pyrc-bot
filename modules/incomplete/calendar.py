import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import icalendar

@module.type("PRIVMSG")
def echo_fn(bot,message,regex_matches=None):
	#bot.commands.privmsg(message.sender,"{}: you said '{}'".format(message.sender,message.message))
	print("{}: you said '{}'".format(message.sender,message.message))

echo = module.Module("echo")
echo.add_function(echo_fn)
