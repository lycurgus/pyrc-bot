import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import re
import util

articles = ["some","the","his","her","their","an","a","another",""]
botnames = ["snuggles","snugglebunny"]
verbs = ["gives","hands","tosses","passes","feeds"]

gift_pattern = r"{1} {2} {0}(.*)|{1} {0}(.*) to {2}".format("".join(["(?:{} )?".format(a) for a in articles]),"(?:{})".format("|".join(verbs)),"(?:{})".format("|".join(botnames)))

@module.timeout("gift")
@module.action
@module.regex(gift_pattern)
def gift_react(bot,message,regex_matches=None):
	gift = [m.strip() for m in regex_matches.groups() if m][0]
	print("gift was {}".format(gift))
	channel = message.channel
	possession_result = re.match(r"(.*)'s (.*)",gift)
	if possession_result:
		if channel and (possession_result.group(1).lower() in util.lower(bot.channels[channel].users.keys())):
			gift = possession_result.group(2)
	if gift.lower() == "pudding":
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"sniffs at the {}".format(gift))
		else:
			bot.commands.action(message.replyto,"opens an eye and considers the {}".format(gift))
		if channel and ("Saoirse" in bot.channels[channel].users.keys()):
			if not bot.getcustom("asleep"):
				bot.commands.action(message.replyto,"gives the {} to Saoirse".format(gift))
			else:
				bot.commands.action(message.replyto,"pushes the {} towards Saoirse".format(gift))
		else:
			friend = "" if channel in ["#limittheory","#goatcasino","#snugglebunny"] else "her friend "
			bot.commands.action(message.replyto,"notices {}Saoirse isn't nearby".format(friend))
			if not bot.getcustom("asleep"):
				bot.commands.action(message.replyto,"eats the {} with delight".format(gift))
			else:
				bot.commands.action(message.replyto,"sets the {} aside for later and goes back to sleep".format(gift))
	elif channel and (gift.lower() in util.lower(bot.channels[channel].users.keys())):
		if gift.lower() == bot.boss:
			bot.commands.action(message.replyto,"nibbles {} gently".format(gift))
		elif gift.lower() in [n.lower() for n in bot.names]:
			eye_open = "" if not bot.getcustom("asleep") else "opens her eye and "
			bot.commands.action(message.replyto,"{}stares at {}".format(eye_open,message.sender))
		else:
			if not bot.getcustom("asleep"):
				if util.chance(0.75):
					bot.commands.action(message.replyto,"squeals in delight")
					bot.commands.action(message.replyto,"opens her terrifying maw")
				bot.commands.action(message.replyto,"eats {} whole".format(gift))
			else:
				bot.commands.action(message.replyto,"sleepily bites {}".format(gift))
	elif gift.lower() in ["hug","hugs"]:
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"hugs {} back".format(message.sender))
		else:
			bot.commands.action(message.replyto,"hugs {} in her sleep".format(message.sender))
	elif re.match(r"\b(?:dick|penis|d|cock|phallus)(?:s|es)?\b",gift.lower()):
		if not bot.getcustom("asleep"):
			bot.commands.privmsg(message.replyto,"{}: http://imgur.com/fy0hSOG".format(message.sender))
		else:
			bot.commands.action(message.replyto,"shifts in her sleep and kicks {} somewhere sensitive".format(message.sender))
	elif gift.lower() == "nothing":
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"doesn't eat it")
	elif gift.lower() == "copypasta":
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"eats the {}".format(gift))
			bot.commands.privmsg(message.replyto,"{}: you're fuckin' dead, kiddo".format(message.sender))
		else:
			bot.commands.action(message.replyto,"ignores the {}".format(gift))
	elif gift.lower() == "carrot":
		if not bot.getcustom("asleep"):
			if util.chance(0.25):
				bot.commands.action(message.replyto,"puts it in a pretty vase")
			else:
				bot.commands.action(message.replyto,"eats the {}".format(gift))
		else:
			bot.commands.action(message.replyto,"smiles in her sleep and cuddles the {}".format(gift))
	elif gift.lower() == "carrots":
		if not bot.getcustom("asleep"):
			if util.chance(0.25):
				bot.commands.action(message.replyto,"puts them in a pretty vase")
			else:
				bot.commands.action(message.replyto,"eats the {}".format(gift))
		else:
			bot.commands.action(message.replyto,"smiles in her sleep and cuddles the {}".format(gift))
	elif gift.lower() in ["a", "the", "."] + [n.lower() for n in bot.names]:
		eye_open = "" if not bot.getcustom("asleep") else "opens her eye and "
		bot.commands.action(message.replyto,"{}stares at {}".format(eye_open,message.sender))
	elif gift.lower() in ["holy hand grenade","holy hand grenade of antioch"]:
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"pulls the pin")
			bot.commands.action(message.replyto,"counts to four^H^H^H^Hthree")
			bot.commands.action(message.replyto,"lobs the grenade back at {}".format(message.sender))
			#cave of caerbannog
			#black beast of arrrghhh
			#vicious streak a mile wide
	elif gift.lower() == "twenty dollars":
		if not bot.getcustom("asleep"):
			bot.commands.privmsg(message.replyto,"aw, twenty dollars? i wanted a carrot :(")
	else:
		if not bot.getcustom("asleep"):
			bot.commands.action(message.replyto,"eats the {}".format(gift))
		else:
			bot.commands.action(message.replyto,"sleepily nibbles the {}".format(gift))

gift = module.Module("gift")
gift.add_function(gift_react)
gift.add_timeout("gift",seconds=5)
