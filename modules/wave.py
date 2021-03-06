import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util

@module.timeout("wave")
@module.type("PRIVMSG")
@module.regex(r"(?:^|.*\s)(o7|o/|\\\o/|\\\o)(?:\s.*|$)")
def wave_respond(bot,message,regex_matches=None):
	wave = regex_matches.group(1)
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,wave)
	elif util.chance(0.2):
		bot.commands.action(message.replyto,"{} sleepily".format("salutes" if wave == "o7" else "waves a paw"))

wave = module.Module("wave")
wave.add_function(wave_respond)
wave.add_timeout("wave",seconds=45)
