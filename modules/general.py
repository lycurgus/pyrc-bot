import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util
import random
from datetime import timedelta

@module.timeout("poop")
@module.command("poop")
def poop(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"     (   )  ")
	bot.commands.privmsg(message.replyto,"  (   ) (   ")
	bot.commands.privmsg(message.replyto,"   ) _   )  ")
	bot.commands.privmsg(message.replyto,"    ( \_    ")
	bot.commands.privmsg(message.replyto,"  _(_\ \)__ ")
	bot.commands.privmsg(message.replyto," (____\___))")

@module.command("beep boop")
@module.user_not_present("taiya")
@module.timeout("beep")
def beep_boop(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"boop beep")

@module.command("pew")
def pew(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		if util.chance(0.01):
			bot.commands.privmsg(message.replyto,"pew pew")

@module.command("carrots")
def carrots(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,"CARROTS!")
	else:
		bot.commands.action(message.replyto,"sleepily extends a paw to receive a carrot")

@module.command("bunny")
def bunny(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"🐇")

@module.timeout("lenny")
@module.command("!lenny")
@module.user_not_present("saoirse")
def lenny(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"( ͡° ͜ʖ ͡°)")

@module.timeout("hello")
@module.regex(r".*\b(?:ohai|hi|hey|hello|hiya|howdy)\b.*")
@module.direct
def greet(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		reply = random.choice([
			"hi {} :)".format(message.sender),
			"hey there!",
			"hiya {}".format(message.sender),
			"hello, {}".format(message.sender)
		])
		bot.commands.privmsg(message.replyto,reply)
	else:
		bot.commands.action(message.replyto,"waves sleepily at {}".format(message.sender))

@module.regex(r"^beep$")
@module.timeout("beep")
def beep(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,"boop")
	else:
		bot.commands.privmsg(message.replyto,"peeps softly in her sleep")

@module.regex(r"^moon$")
def moon(bot,message,regex_matches=None):
	if not bot.getcustom("asleep") or (util.chance(0.25)):
		bot.commands.privmsg(message.replyto,"hlör u fang axaxaxas mlö")
		c = {
			'nick': bot.boss,
			'type': 'NOTICE'
			}
		a = [bot.commands.privmsg]
		p = [[bot.boss,"hi this is an expectation-dependent response wow!"]]
		ea = [bot.commands.privmsg]
		ep = [[bot.boss,"you never got back to me! :<"]]
		if line.nick == bot.boss:
			bot.expectations.append(Expectation(c,a,p,timedelta(minutes=1),ea,ep))

@module.regex(r"^cani\?$")
def cani(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"http://imgur.com/fy0hSOG")

@module.regex(r".*what do you look like\?")
@module.direct
def picture_of_self(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"http://i.imgur.com/96XolVw.jpg")

@module.regex(r"^!pwn (.*)$")
def pwn_response(bot,message,regex_matches=None):
	if regex_matches.group(1) in bot.names:
		#print("someone tried to have me kicked :<")
		bot.commands.privmsg(message.replyto,"!pwn {}".format(message.sender))
		bot.commands.privmsg(message.replyto,":V")

@module.regex(r"drags a rabbit up onto a stone slab")
@module.action
def dont_sacrifice_bunny(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		responses = {
				'say': [
					"i don't like that one bit, sir",
					"{} violence against rabbits!".format(random.choice(["stop","end","no more"])),
					"you stop that, {}".format(message.sender)
				],
				'do': [
					"glares at {}".format(message.sender),
					"reports {} to PETA".format(message.sender)
				]
			}
		selection = random.choice(responses.keys())
		if selection == 'say':
			bot.commands.privmsg(message.replyto,random.choice(responses['say']))
		else:
			bot.commands.action(message.replyto,random.choice(responses['do']))
	else:
		if util.chance(0.6):
			bot.commands.action(message.replyto,"frowns in her sleep")

@module.admin
@module.regex(r"^away: (.*)$")
def set_away(bot,message,regex_matches=None):
	bot.commands.away(regex_matches.group(1))

@module.admin
@module.regex(r"^away: (.*)$")
def set_back(bot,message,regex_matches=None):
	bot.commands.unaway(bot.nick)

def rollcall():
	if True:
		pass
	elif line.rest.lower() in ["bots, roll call","bots: roll call","who here is a bot?","who are the bots?","who here is a bot","who are the bots"]:
		if not bot.getcustom("asleep"):
			bot.commands.action(replyto,"raises a paw")
			bot.commands.privmsg(replyto,":)")
		else:
			bot.commands.action(replyto,"raises a paw sleepily")


@module.action
@module.regex(r"pokes ([^\b]*)(?:\b .*)")
def poked(bot,message,regex_matches=None):
	if not regex_matches.group(1).lower() in list(map(str.lower,bot.names)):
		return
	if not bot.getcustom("asleep"):
		bot.commands.action(message.replyto,random.choice(["squeaks adorably","glares adorably at {}".format(message.sender)]))
	else:
		bot.commands.action(message.replyto,random.choice(["squirms in her sleep","snores"]))

@module.sender("taiya")
@module.action
@module.regex(r"puts him in a pretty vase")
def vase_rescue(bot,message,regex_matches=None):
	print("someone is in a vase")
	if not bot.getcustom("asleep"):
		if util.chance(0.4):
			bot.commands.action(replyto,"waddles up to the vase")
			bot.commands.action(replyto,"stands on her hind legs")
			bot.commands.action(replyto,"knocks the vase over")
		elif util.chance(0.05):
			bot.commands.action(replyto,"helpfully adds water to the vase")
			bot.commands.privmsg(replyto,":)")
	else:
		if util.chance(0.2):
			sleepy_vase_breaker = random.choice(["tosses a pillow at the vase to knock it over","rolls over in her sleep and knocks the vase over"])
			bot.commands.action(replyto,sleepy_vase_breaker)

@module.direct
@module.regex(r"who(?:'s| is) your (?:boss|owner)\??")
def boss_report(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"it's {}".format(bot.boss))

@module.sender("taiya")
@module.regex(r"this too shall pass")
def this_too(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"https://www.youtube.com/watch?v=qybUFnY7Y8w")

@module.direct
@module.disable
@module.regex(r"login .*")
def whats_a_login(bot,message,regex_matches=None):
	print('login attempt')
	print(message.message)
	bot.commands.privmsg(message.replyto,"uhh, okay!")
	bot.commands.action(message.replyto,"pretends to understand")
	bot.commands.action(message.replyto,"shuffles some papers around")

@module.direct
#@module.disable
@module.regex(r"are you a (?:boy|girl)(?: or a (?:girl|boy))?\??")
def professor_oak(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		bot.commands.privmsg(message.replyto,"i'm a doe :)")
	else:
		bot.commands.action(message.replyto,"waves her paw dismissively at {}".format(message.sender))

@module.regex(r"module report")
@module.admin
def module_report(bot,message,regex_matches=None):
	print('modules:')
	print('{} loaded'.format(len(bot.loadedmodules)))
	print('{} failed'.format(len(bot.failedmodules)))
	if len(bot.failedmodules):
		bot.commands.privmsg('failed modules: {}'.format(' ,'.join(bot.failedmodules)))

general = module.Module("general")
general.add_function(poop)
general.add_timeout("poop",minutes=3)
general.add_function(beep_boop)
general.add_timeout("beep",minutes=1)
general.add_function(beep)
general.add_function(pew)
general.add_function(carrots)
general.add_function(bunny)
general.add_timeout("lenny",seconds=20)
general.add_function(lenny)
general.add_timeout("hello",seconds=15)
general.add_function(greet)
general.add_function(moon)
general.add_function(cani)
general.add_function(picture_of_self)
general.add_function(pwn_response)
general.add_function(dont_sacrifice_bunny)
general.add_function(vase_rescue)
general.add_function(boss_report)
general.add_function(this_too)
general.add_function(whats_a_login)
general.add_function(professor_oak)
general.add_function(module_report)
