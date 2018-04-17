import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.type("PRIVMSG")
def greet_new_person(bot,message,regex_matches=None):
	if not message.channel:
		return
	ai = bot.channels[message.channel].activityindex
	if ai == 0:
		if message.sender not in bot.known_users:
			bot.commands.privmsg(message.replyto,"hi there {} - are you new?".format(message.sender))
			bot.commands.privmsg(message.replyto,"(i'm a bot, but it looks like nobody else is around at the moment so i thought i should say hi)")

newperson = module.Module("newperson")
newperson.add_function(greet_new_person)
