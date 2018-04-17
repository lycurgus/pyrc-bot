import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta

class Blackjack:
	pass

def blackjack_setup(bot):
	bot.registercustom('blackjack',None)
	bot.setcustom('blackjack',Blackjack())

#@module.timeout(timedelta(hours=1),"echo")
@module.type("PRIVMSG")
def echo_fn(bot,message,regex_matches=None):
	print("{}: you said '{}'".format(message.sender,message.message))

blackjack = module.Module("blackjack")
blackjack.add_function(handle_game)
blackjack.setup_function = blackjack_setup
