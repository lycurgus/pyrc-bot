import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util

@module.regex(r"(.*),? help")
@module.direct
@module.timeout("help")
@module.type("PRIVMSG")
def help_reply(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if not message.replyto == message.sender:
		"i'll PM you, {}".format(message.sender)
	#"you're on your own for now, {} - ask {} and he can give you an overview".format(line.nick,bot.boss)
	helpmessages = [
		"hi! so i'm SnuggleBunny; i'm a bot (you knew that, right?)",
		"i can do a few things - some of them useful - but i don't have a list of them yet. i'm sure you can figure them out :)",
		"if you have any questions or suggestions (in particular, something you think i should do, or that i do wrong at the moment), let {} know".format(bot.boss),
		"someday i'll be able to handle those sorts of things myself and pass them on! but for now my abilities are pretty limited :)"
	]
	for i,m in enumerate(helpmessages):
		mn = "[{}/{}] {}".format(i+1,len(helpmessages),m)
		bot.commands.privmsg(message.sender,mn)
	#"{} is the one responsible for me, so for now you'll have to take any questions or suggestions to him.".format(bot.boss)

help_msg = module.Module("help_msg")
help_msg.add_function(help_reply)
help_msg.add_timeout("help",minutes=2)
