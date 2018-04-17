import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import random
import util

@module.type("PRIVMSG")
@module.regex(r"(?:(?:g?'?|good)? ?morning),?.*? ([^\b]+?)\b.*")
def good_morning(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if not bot.timeout("justwokeorslept").get() and bot.awake:
		replies = [
				"good morning! :)",
				"g'morning, {}!".format(message.sender),
				"good morning :)",
				":)"
			]
		bot.commands.privmsg(message.replyto,random.choice(replies))

@module.type("PRIVMSG")
@module.regex(r"(?:(?:g?'?|good)? ?night),?.*? ([^\b]+?)\b.*")
def good_night(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		return
	if not bot.timeout("justwokeorslept").get() and not bot.awake:
		actions = [
				"mumbles a sleepy thankyou",
				"smiles and snuggles into the sheets",
				"snores softly"
			]
		bot.commands.action(message.replyto,random.choice(actions))

goodmorning = module.Module("goodmorning")
goodmorning.add_function(good_morning)
goodmorning.add_function(good_night)
