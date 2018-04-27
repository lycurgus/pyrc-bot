import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random

@module.type("PRIVMSG")
@module.regex(r"^\!coin(?:flip)?")
def coinflip_fn(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,random.choice(("heads!","tails!")))

coinflip = module.Module("coinflip")
coinflip.add_function(coinflip_fn)
