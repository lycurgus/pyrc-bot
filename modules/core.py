import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import re
from datetime import datetime, timedelta
from util import Channel, NickStatus, Expectation
from blinker import signal
from writer import Writer

#TODO define the base tick as a timed function....?
#TODO (need a spot to put these notes!)
#TODO add language/translation ability for strings? snuggles should (be able to) speak jäger
#idea: a module can either hardcode things or define strings to be added to the bot instance?
#idea: a separate file for modules' strings?

w = Writer()

@module.type("PRIVMSG")
def resp_privmsg(bot,message,regex_matches=None):
	line_format = "${{dark_blue}}{u}${{reset}} (${{{clr}}}{s}{sep}{c}${{reset}}): {ast}{l}"
	parts = {
			'u': message.nick,
			'clr': 'light_red' if bot.being_addressed(message) else 'reset',
			's': bot.servername,
			'sep': '' if message.parameters[0].startswith('#') else ':',
			'c': message.parameters[0],
			'ast': '* ' if message.is_action else '',
			'l': re.sub(r"({})".format("|".join(bot.names)),r"${light_green}\1${reset}",message.message,flags=re.IGNORECASE)
		}
	w.write(line_format.format(**parts))
	channel = message.channel
	if channel:
		if message.nick not in bot.channels[channel].users.keys():
			bot.channels[channel].add_user(message.nick)
		bot.channels[channel].line_seen()
		bot.channels[channel].users[message.nick].talked(message.message)

@module.type("QUIT")
def handle_quitreport(bot,message,regex_matches=None):
	user = message.nick
	reason = message.message
	if reason == "Registered":
		print("user {} registered".format(user))
		return
	print("user {} is quitting".format(user))
	for cname,channel in bot.channels.items():
		bot.channels[cname].remove_user(user)

@module.type("JOIN")
def handle_joinreport(bot,message,regex_matches=None):
	channel = message.message
	joiner = message.nick
	if channel:
		w.write("${{light_blue}}{}${{reset}} joined ${{light_green}}{}${{reset}}".format(joiner,channel))
		if channel not in bot.channels.keys():
			bot.channels[channel] = Channel(channel)
		bot.channels[channel].add_user(joiner)

@module.type("PART")
def handle_partreport(bot,message,regex_matches=None):
	channel = message.channel
	if not channel:
		print(message.raw)
	print("user {} left {}".format(message.nick,channel))
	if channel in bot.channels.keys():
		if message.nick in bot.channels[channel].users.keys():
			del bot.channels[channel].users[message.nick]

@module.type("NICK")
def handle_nickreport(bot,message,regex_matches=None):
	oldnick = message.nick
	newnick = message.message
	print("user {} changing nick to {}".format(oldnick,newnick))
	if oldnick == bot.boss:
		bot.boss = newnick
	for channel in bot.channels.keys():
		bot.channels[channel].rename_user(oldnick,newnick)

@module.type("INVITE")
def handle_invite(bot,message,regex_matches=None):
	#:lycurgus!lycurgus@gamesurge-a402b724.gs INVITE SnuggleBunny #limittheory
	chan = message.channel
	if message.nick == bot.boss:
		bot.commands.join(chan)
	else:
		bot.commands.privmsg(message.nick,"hang on, i have to ask the boss :)")
		bot.commands.privmsg(bot.boss,"{} wanted me to join {}.... is that okay?".format(message.nick,chan))
		c = {
				'nick': bot.boss,
				'or': ["yes","ok","sure","fine"],
				'not': ["no","not"]
			}
		a = [bot.commands.join]
		p = [[chan]]
		e = timedelta(minutes=10)
		ea, ep = [bot.commands.privmsg], [[message.nick,"sorry, my boss didn't want me to join"]] #expiry actions, expiry parameters
		bot.expectations.append(Expectation(bot,c,a,p,e,ea,ep))

@module.type("KICK")
def handle_kick(bot,message,regex_matches=None):
	channel = message.channel
	kicked = message.parameters[1]
	reason = message.message
	if kicked == bot.nick:
		bot.commands.privmsg(bot.boss,"i got kicked from {} ({})".format(channel,reason))
	else:
		bot.channels[channel].remove_user(kicked)

@module.type("NOTICE")
def resp_notice(bot,message,regex_matches=None):
	if message.nick != "Global":
		print("{} {} {} {}".format(message.nick,message.command,message.parameters[0],message.message))

@module.type("ERROR")
def resp_err(bot,message,regex_matches=None):
	w.write("{} ${{dark_red}}{}${{reset}} {} {}".format(message.nick,message.command,message.parameters[0],message.message))

@module.type("PING")
def resp_ping(bot,message,regex_matches=None):
	w.write('${{light_red}}{}${{reset}} -- got ping, sending pong'.format(datetime.now()))
	bot.commands.pong(message.message)

@module.type("MODE")
def resp_mode(bot,message,regex_matches=None):
	if message.parameters[0] == bot.nick: #usermode
		mode = message.message[0]
		for c in message.message[1:]:
			if mode == "+":
				bot.modes.append(c)
				print("received mode {}".format(c))
			else:
				bot.modes = [m for m in bot.modes if m != c]
				print("lost mode {}".format(c))
		if "r" in bot.modes: #nickserv registration came in
			bot.ns_registered = True
			for channel in bot.channels_awaiting_auth:
				bot.commands.join(channel)
	else: #channel mode
		channel = message.parameters[0]
		mode = message.parameters[1]
		args = message.parameters[2:]
		print("mode {} received for {}. arguments: {}".format(mode,channel,args))
		bot.channels[channel].modes.add((mode,args)) #TODO confirm this is workable

@module.type("001")
def connected(bot,message,regex_matches=None):
	bot.connected = True
	for chan in bot.autochannels:
		if chan in bot.ignoreautojointemp:
			continue
		bot.commands.join(chan)
	signal("SUPER").send(None,act="bot_instance",params={
		'name': bot.servername,
		'bot':  bot
		})
	bot.commands.privmsg(bot.boss,"hi!")
	bot.commands.privmsg(bot.boss,"m: ${{light_green}}{}${{reset}} // f: ${{light_red}}{}${{reset}}".format(len(bot.loadedmodules),len(bot.failedmodules)))

@module.type("002") #your host is
def yourhost(bot,message,regex_matches=None):
	pass

@module.type("003") #server created
def msg_003(bot,message,regex_matches=None):
	pass

@module.type("005") #supported commands
def msg_005(bot,message,regex_matches=None):
	for p in message.parameters[1:]:
		if "=" in p: #key-value
			kv = p.split("=",1)
			bot.servermodes[kv[0]] = kv[1]
		else:
			bot.servermodes[p] = True

@module.type("301") #user is away
def msg_301(bot,message,regex_matches=None):
	print("user {} is away: {}".format(message.parameters[1],message.message))

@module.type("311") #RPL_WHOISUSER
def read_whoisuser(bot,message,regex_matches=None):
	user = message.parameters[0]
	status = NickStatus(True)
	bot.seen_users[user] = status

@module.type("332") #channel topic
def read_chantopic(bot,message,regex_matches=None):
	channel = message.parameters[1]
	if channel not in bot.channels.keys():
		bot.channels[channel] = Channel(channel)
	bot.channels[channel].topic = message.message

@module.type("353") #channel names list
def handle_nameslist(bot,message,regex_matches=None):
	nameslist = [n.lstrip("@%+~&") for n in message.message.split(" ")]
	channel = message.parameters[-1]
	flagname = "names_{}".format(channel)
	customname = "seen_users_{}".format(channel)
	if bot.flags(flagname) == False: #this is the first RPL_NAMREPLY
		bot.setcustom(customname,nameslist)
		if channel not in bot.channels.keys():
			print("adding channel: {}".format(channel))
			bot.channels[channel] = Channel(channel)
		else:
			print("got updated names for {}".format(channel))
			chanusers = list(bot.channels[channel].users.keys())
			for name in nameslist:
				if not name in chanusers:
					bot.channels[channel].add_user(name)
		bot.flags(flagname,True)
	else: #this is a subsequent RPL_NAMREPLY
		chanusers = list(bot.channels[channel].users.keys())
		existing_seen = bot.getcustom(customname)
		bot.setcustom(customname,nameslist+existing_seen)
		for name in nameslist:
			if not name in chanusers:
				bot.channels[channel].add_user(name)
	c = { 'type': '366' }
	a = []
	p = [[]]
	e = timedelta(minutes=5)
	ea = [bot.flags,bot.removecustom]
	ep = [[flagname,False],[customname]]
	bot.expectations.append(Expectation(bot,c,a,p,e,ea,ep))

@module.type("366") #end of names list
def handle_endofnameslist(bot,message,regex_matches=None):
	channel = message.parameters[-1]
	flagname = "names_{}".format(channel)
	customname = "seen_users_{}".format(channel)
	bot.flags(flagname,False)
	nameslist = bot.getcustom(customname)
	chanusers = list(bot.channels[channel].users.keys())
	for user in chanusers:
		if user not in nameslist:
			bot.channels[channel].remove_user(name)
	bot.removecustom(customname)
	print("got RPL_ENDOFNAMES for {}".format(channel))

@module.type("401") #ERR_NOSUCHNICK
def read_whoiserror(bot,message,regex_matches=None):
	user = message.parameters[0]
	status = NickStatus(False)
	bot.seen_users[user] = status

@module.type("433") #nickname in use #:cherryh.freenode.net 433 * SnuggleBunny :Nickname is already in use.
def nickname_in_use(bot,message,regex_matches=None):
	bot.nick = bot.get_alternate_nick(bot.nick) #TODO make this a thing!
	bot.commands.nick(bot.nick)
	bot.commands.privmsg(bot.boss,"hey! my usual nick was in use...")

@module.type("477") #need to be registered to join channel
def ns_identify(bot,message,regex_matches=None):
	channel = message.parameters[1]
	if channel not in bot.channels_awaiting_auth:
		bot.channels_awaiting_auth.append(channel) #for later use when authed
	if bot.ns_pass:
		if not bot.ns_registered and not bot.ns_ident_sent:
			bot.commands.privmsg("nickserv","identify {}".format(bot.ns_pass))
			bot.ns_ident_sent = True
	else:
		bot.commands.privmsg(bot.boss,"i need a nickserv registration to join {}".format(channel))

core = module.Module("core")
core.add_function(resp_privmsg)
core.add_function(handle_quitreport)
core.add_function(handle_joinreport)
core.add_function(handle_partreport)
core.add_function(handle_nickreport)
core.add_function(handle_invite)
core.add_function(handle_kick)
core.add_function(resp_notice)
core.add_function(resp_err)
core.add_function(resp_ping)
core.add_function(resp_mode)
core.add_function(connected)
core.add_function(yourhost)
core.add_function(msg_003)
core.add_function(msg_005)
core.add_function(msg_301)
core.add_function(read_chantopic)
core.add_function(handle_nameslist)
core.add_function(nickname_in_use)
core.add_function(ns_identify)
