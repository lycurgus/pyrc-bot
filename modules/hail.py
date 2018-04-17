import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.command(["all hail! /o/","all hail"])
@module.timeout("hail")
def all_hail(bot,message,regex_matches=None):
	if bot.awake:
		bot.commands.privmsg(message.replyto,"All hail! /o/")

hail = module.Module("hail")
hail.add_function(all_hail)
hail.add_timeout("hail",seconds=30)
