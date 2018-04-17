import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from random import choice

@module.type("PRIVMSG")
@module.command(["!coin","!coinflip"])
def coinflip_fn(bot,line,regex_matches=None):
	replyto = line.replyto
	bot.commands.privmsg(replyto,choice(("heads!","tails!")))

coinflip = module.Module("coinflip")
coinflip.add_function(coinflip_fn)
