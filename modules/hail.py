import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module

@module.command(["all hail! /o/","all hail"])
@module.timeout("hail")
def all_hail(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,"All hail! /o/")

hail = module.Module("hail")
hail.add_function(all_hail)
hail.add_timeout("hail",seconds=30)
