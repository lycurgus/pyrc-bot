import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from datetime import timedelta, datetime
import random
import util
import re

@module.timer("breaksilence")
def break_silence(bot,message,regex_matches=None):
	if len(list(bot.channels.keys())) == 0:
		return
	channel = random.choice(list(bot.channels.keys()))
	if not bot.getcustom("asleep"):
		actions = [
				"flicks her ears",
				"twitches her nose",
				"looks around for anyone to play with",
				"looks around for someone to play with",
				"hops around a bit",
				"hums a tune",
				"quacks"
			]
		if "taiya" in util.lower(bot.channels[channel].users.keys()):
			actions.append("gives Taiya flowers")
			actions.append("gives Taiya a hug")
		if 12 < datetime.now().hour < 20:
			actions.append("sips a piña colada")
	else:
		actions = [
				"snores",
				"tosses in her sleep",
				"squeaks adorably",
				"giggles in her sleep",
				"mutters in her sleep",
				"smiles at something in her dream"
			]
	if util.chance(0.75) and (bot.channels[channel].activityindex == 0):
		act = random.choice(actions)
		bot.commands.action(channel,act)
		if act == "quacks":
			bot.commands.privmsg(channel,"... wait, what?")
		elif (act == "looks around for anyone to play with") or (act == "looks around for someone to play with"):
			c = {
					'type': 'PRIVMSG',
					'action': True,
					'regex': re.compile(r"^.*play.*_BOTNAMES_.*$")
				}
			a = [bot.commands.action]
			p = [[channel,"giggles delightedly"]]
			e = timedelta(minutes=2)
			bot.expectations.append(util.Expectation(bot,c,a,p,e))

breaksilence = module.Module("breaksilence")
breaksilence.add_function(break_silence)
breaksilence.add_timer("breaksilence",hours=2)
