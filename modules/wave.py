import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util
#from util import chance
#from datetime import timedelta

@module.timeout("wave")
@module.type("PRIVMSG")
@module.regex(r"(?:^|.*\s)(o7|o/|\\\o/|\\\o)(?:\s.*|$)")
def wave_respond(bot,message,regex_matches=None):
	wave = regex_matches.group(1)
	if bot.awake:
		bot.commands.privmsg(message.replyto,wave)
	elif util.chance(0.2):
		bot.commands.action(message.replyto,"{} sleepily".format("salutes" if wave == "o7" else "waves a paw"))

wave = module.Module("wave")
wave.add_function(wave_respond)
wave.add_timeout("wave",seconds=45)
