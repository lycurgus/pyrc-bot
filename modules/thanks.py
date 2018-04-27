import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util
import random

@module.regex(r"^(?:thanks|thank you|thx),? ([^\b]+?)\b.*")
@module.type("PRIVMSG")
def youre_welcome(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in util.lower(bot.names):
		#print('person being thanked was: {}'.format(regex_matches.group(1)))
		return
	if not bot.getcustom("asleep"):
		thanks = random.choice(["you're welcome","no problem","sure thing","any time"])
		target = ""
		if util.chance(0.3):
			target = ", {}".format(message.sender)
		emote = ""
		if util.chance(0.6):
			emote = random.choice([" :)","!"," :3"])
		bot.commands.privmsg(message.replyto,"{}{}{}".format(thanks,target,emote))
	else:
		if util.chance(0.2):
			bot.commands.action(message.replyto,"waves a paw at {}".format(message.sender))
		elif util.chance(0.5):
			bot.commands.action(message.replyto,"snores")

thanks = module.Module("thanks")
thanks.add_function(youre_welcome)
