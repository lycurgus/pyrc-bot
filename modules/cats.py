import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util

@module.timeout("meow")
@module.type("PRIVMSG")
@module.regex(r"\bmeow\b")
def react_cat(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		if util.chance(0.3):
			bot.commands.privmsg(message.replyto,"oh no, a cat!")
			bot.commands.action(message.replyto,"runs and hides")
		elif util.chance(0.6):
			bot.commands.privmsg(message.replyto,"a kitty!")
			bot.commands.action(message.replyto,"snuggles the kitty")

cats = module.Module("cats")
cats.add_function(react_cat)
cats.add_timeout("meow",seconds=10)
