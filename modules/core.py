import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import re
from datetime import datetime
from util import Channel, NickStatus
from blinker import signal

#TODO define the base tick as a timed function....?
#TODO (need a spot to put these notes!)
#TODO add language/translation ability for strings? snuggles should (be able to) speak jäger
#idea: a module can either hardcode things or define strings to be added to the bot instance?
#idea: a separate file for modules' strings?

@module.line
@module.type("PRIVMSG")
def resp_privmsg(bot,line,regex_matches=None):
	print("{u} ({s}{sep}{c}): {l}".format(u=line.nick,s=bot.servername,sep='' if line.parameters[0].startswith('#') else ':',c=line.parameters[0],l=line.rest))
	channel = line.parameters[0] if not line.parameters[0] == bot.nick else None
	if channel:
		if line.nick not in bot.channels[channel].users.keys():
			bot.channels[channel].add_user(line.nick)
		bot.channels[channel].line_seen()
		bot.channels[channel].users[line.nick].talked(line.rest)
	if bot.being_addressed(line):
		print('being addressed')

@module.line
@module.type("QUIT")
def handle_quitreport(bot,line,regex_matches=None):
	print("user {} is quitting".format(line.nick))
	for cname,channel in bot.channels.items():
		bot.channels[cname].remove_user(line.nick)

@module.line
@module.type("JOIN")
def handle_joinreport(bot,line,regex_matches=None):
	channel = line.rest
	joiner = line.nick
	if channel and not (joiner == bot.nick):
		print("{} joined {}".format(joiner,channel))
		bot.channels[channel].add_user(joiner)

@module.line
@module.type("PART")
def handle_partreport(bot,line,regex_matches=None):
	channel = line.parameters[0]
	if not channel:
		print(line.line['raw'])
	reason = line.rest
	print("user {} left {}".format(line.nick,channel))
	if channel in bot.channels.keys():
		if line.nick in bot.channels[channel].users.keys():
			del bot.channels[channel].users[line.nick]

@module.line
@module.type("NICK")
def handle_nickreport(bot,line,regex_matches=None):
	oldnick = line.nick
	newnick = line.rest
	print("user {} changing nick to {}".format(oldnick,newnick))
	if oldnick == bot.boss:
		bot.boss = newnick
	for cname,channel in bot.channels.items():
		bot.channels[cname].rename_user(oldnick,newnick)

@module.line
@module.type("INVITE")
def handle_invite(bot,line,regex_matches=None):
	#:lycurgus!lycurgus@gamesurge-a402b724.gs INVITE SnuggleBunny #limittheory
	chan = line.parameters[0]
	if line.nick == bot.boss:
		bot.commands.join(chan)
	else:
		bot.commands.privmsg(line.nick,"hang on, i have to ask the boss :)")
		bot.commands.privmsg(bot.boss,"{} wanted me to join {}.... is that okay?".format(line.nick,chan))
		c = {
				'nick': bot.boss,
				'or': ["yes","ok","sure","fine"],
				'not': ["no","not"]
			}
		a = [bot.commands.join]
		p = [[chan]]
		e = timedelta(minutes=10)
		ea, ep = [bot.commands.privmsg], [[line.nick,"sorry, my boss didn't want me to join"]] #expiry actions, expiry parameters
		bot.expectations.append(Expectation(c,a,p,e,ea,ep))

@module.line
@module.type("KICK")
def handle_kick(bot,line,regex_matches=None):
	channel = line.parameters[0]
	kicked = line.parameters[1]
	reason = line.rest
	if kicked == bot.nick:
		bot.commands.privmsg(bot.boss,"i got kicked from {} ({})".format(channel,reason))
	else:
		bot.channels[channel].remove_user(kicked)

@module.line
@module.type("NOTICE")
def resp_notice(bot,line,regex_matches=None):
	if line.nick != "Global":
		print("{} {} {} {}".format(line.nick,line.command,line.parameters[0],line.rest))

@module.line
@module.type("ERROR")
def resp_err(bot,line,regex_matches=None):
	print("{} {} {} {}".format(line.nick,line.command,line.parameters[0],line.rest))

@module.line
@module.type("PING")
def resp_ping(bot,line,regex_matches=None):
	print('{} -- got ping, sending pong'.format(datetime.now()))
	bot.commands.pong(line.rest)

@module.line
@module.type("MODE")
def resp_mode(bot,line,regex_matches=None):
	if line.parameters[0] == bot.nick: #usermode
		mode = line.rest[0]
		for c in line.rest[1:]:
			if mode == "+":
				bot.modes.append(c)
			else:
				bot.modes = [m for m in bot.modes if m != c]
		if "r" in bot.modes: #nickserv registration came in
			bot.ns_registered = True
			for channel in bot.channels_awaiting_auth:
				bot.commands.join(channel)
	else: #channel mode
		channel = line.parameters[0]
		mode = line.parameters[1]
		args = line.parameters[2:]
		bot.channels[channel].modes.add((mode,args)) #TODO confirm this is workable

@module.line
@module.type("001")
def connected(bot,line,regex_matches=None):
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

@module.line
@module.type("002") #your host is
def yourhost(bot,line,regex_matches=None):
	pass

@module.line
@module.type("003") #server created
def msg_003(bot,line,regex_matches=None):
	pass

@module.line
@module.type("005") #supported commands
def msg_005(bot,line,regex_matches=None):
	#print(line.parameters[1:])
	for p in line.parameters[1:]:
		if "=" in p: #key-value
			kv = p.split("=",1)
			bot.servermodes[kv[0]] = kv[1]
		else:
			bot.servermodes[p] = True

@module.line
@module.type("301") #user is away
def msg_301(bot,line,regex_matches=None):
	print("user {} is away: {}".format(line.parameters[1],line.rest))

@module.line
@module.type("311") #RPL_WHOISUSER
def read_whoisuser(bot,line,regex_matches=None):
	user = line.parameters[0]
	status = NickStatus(True)
	bot.seen_users[user] = status

@module.line
@module.type("332") #channel topic
def read_chantopic(bot,line,regex_matches=None):
	channel = line.parameters[1]
	if channel not in bot.channels.keys():
		bot.channels[channel] = Channel(channel)
	bot.channels[channel].topic = line.rest

@module.line
@module.type("353") #channel names list
def handle_nameslist(bot,line,regex_matches=None):
	nameslist = [n.lstrip("@%+~&") for n in line.rest.split(" ")]
	channel = line.parameters[-1]
	if channel not in bot.channels.keys():
		print("adding channel: {}".format(channel))
		bot.channels[channel] = Channel(channel)
	else:
		print("got updated names for {}".format(channel))
	chanusers = bot.channels[channel].users.keys()
	for name in nameslist:
		if not name in chanusers:
			#bot.channels[channel].add_user(name.lstrip("@%+~&"))
			bot.channels[channel].add_user(name)
	for user in chanusers: #TODO dictionary size changed during iteration - needs a clone??
		if user not in nameslist:
			bot.channels[channel].remove_user(name)
	before = len(chanusers)
	after = len(nameslist)
	if before != after:
		print("{0} had {1} users, now has {2} ({3:+d})".format(channel,before,after,after-before))
		if before > after:
			print("channel users: {}".format(", ".join(chanusers)))
			print("listed users: {}".format(", ".join(nameslist)))
			print("{} left unnoticed".format(", ".join([d for d in chanusers if d.lower() not in [nl.lower() for nl in nameslist]])))
		else:
			print("{} joined unnoticed".format(", ".join([s for s in nameslist if s.lower() not in [cu.lower() for cu in chanusers]])))

@module.line
@module.type("401") #ERR_NOSUCHNICK
def read_whoiserror(bot,line,regex_matches=None):
	user = line.parameters[0]
	status = NickStatus(False)
	bot.seen_users[user] = status

@module.line
@module.type("433") #nickname in use
def nickname_in_use(bot,line,regex_matches=None):
	#:cherryh.freenode.net 433 * SnuggleBunny :Nickname is already in use.
	bot.nick = bot.get_alternate_nick(bot.nick) #TODO make this a thing!
	bot.commands.nick(bot.nick)
	bot.commands.privmsg(bot.boss,"hey! my usual nick was in use...")

@module.line
@module.type("477") #need to be registered to join channel
def ns_identify(bot,line,regex_matches=None):
	channel = line.parameters[1]
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
