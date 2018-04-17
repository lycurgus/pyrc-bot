import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import random
from blinker import signal

@module.regex(r'^join (#[^\s]*)$')
@module.admin
@module.type("PRIVMSG")
def bot_join(bot,message,regex_matches=None):
	if regex_matches:
		new_channel = regex_matches.group(1)
		bot.commands.join(new_channel)

@module.regex(r'^part (#[^\s]*)$')
@module.admin
@module.type("PRIVMSG")
def bot_part(bot,message,regex_matches=None):
	if regex_matches:
		channel = regex_matches.group(1)
	else:
		channel = message.channel
	if channel:
		bot.commands.part(channel)
		del bot.channels[channel]

@module.regex(r'^quit(?: :(.*))?$')
@module.admin
@module.type("PRIVMSG")
def bot_quit(bot,message,regex_matches=None):
	if regex_matches:
		quitmessage = regex_matches.group(1)
	if not quitmessage:
		quitmessage = ""
	#if ":" in message.message:
	#	quitmessage = line.rest.split(":",1)[1].strip()
	if len(quitmessage) == 0:
		quitmessage = "boss told me to!"
	if bot.awake:
		bot.commands.privmsg(message.replyto,"bye!")
	else:
		words = ["knitting","sitting","fitting","quitting"]
		bot.commands.action(message.replyto,"mumbles something about {}".format(random.choice(words)))
	signal("SUPER").send(None,act="set_auto",params={
			'name': bot.servername,
			'auto': False
			})
	bot.quit = True
	bot.commands.quit(quitmessage)

@module.timer("channelcheck")
def check_channel_members(bot,message,regex_matches=None):
	channels = list(bot.channels.keys())
	#print("requesting channel members for:\n{}".format(", ".join(channels)))
	bot.commands.names(channels)

@module.regex(r'^connect (.*)(?: (.*) (.*))?$')
@module.admin
@module.direct
@module.type("PRIVMSG")
def bot_connect(bot,message,regex_matches=None):
	return #TODO connect to a server
	server = None
	host = None
	port = None
	if len(regex_matches.groups) == 1:
		server = regex_matches.group(1)
	elif len(regex_matches.groups) == 3:
		server = regex_matches.group(1)
		host = regex_matches.group(2)
		port = regex_matches.group(3)
	if not host:
		c = bot.db.cursor()
		c.row_factory = sqlite3.Row
		s = c.execute("SELECT name,host,port FROM servers WHERE name = (?)",[server]).fetchone()
		if s:
			host = s['host']
			port = s['port']
	if server and host and port:
		bot.commands.privmsg(message.replyto,"ok, connecting to {}!".format(server))
		signal("SUPER").send(None,act="connect",params={
			'name': server,
			'host': host,
			'port': port,
			'auto': False
			})

@module.regex(r'^connect (.*)(?: (.*) (.*))?$')
@module.not_admin
@module.direct
@module.type("PRIVMSG")
def unauthorised_connect(bot,message,regex_matches=None):
	if bot.awake:
		bot.commands.privmsg(message.replyto,"you're not the boss of me, {}".format(message.sender))
	else:
		bot.commands.action(message.replyto,"rolls over in her sleep to ignore {}".format(message.sender))

@module.regex(r'^disconnect(?: (.*))?$')
@module.admin
@module.direct
@module.type("PRIVMSG")
def bot_disconnect(bot,message,regex_matches=None):
	if len(regex_matches.groups) > 0:
		server = regex_matches.group(1)
	else:
		server = bot.servername
	signal("SUPER").send(None,act="set_auto",params={
		'name': server,
		'auto': False
		})
	bot.commands.privmsg(replyto,"okay, disconnecting from {}".format(server))
	signal("SUPER").send(None,act="disconnect",params={
		'name': server
		})

@module.regex(r'^disconnect(?: (.*))?$')
@module.not_admin
@module.direct
@module.type("PRIVMSG")
def unauthorised_disconnect(bot,message,regex_matches=None):
	if bot.awake:
		bot.commands.privmsg(replyto,"you're not the boss of me, {}".format(line.nick))
	else:
		bot.commands.action(replyto,"rolls over in her sleep to ignore {}".format(line.nick))

@module.direct
@module.regex(r"how active is (#.*)\??")
def activity_report(bot,message,regex_matches=None):
	target = regex_matches.group(1)
	if target in bot.channels.keys():
		ai = bot.channels[target].activityindex
		print(ai)
		if bot.awake:
			bot.commands.privmsg(message.replyto,"i'd call it about a {}".format(round(ai)))
		else:
			bot.commands.action(message.replyto,"stirs from sleep to hold up a sign saying {}".format(round(ai)))

@module.direct
@module.regex(r"user report")
def user_report(bot,message,regex_matches=None):
	for c in bot.channels.keys():
		print("{}: {}".format(c,repr(bot.channels[c].users)))


channels = module.Module("channels")
channels.add_function(bot_join)
channels.add_function(bot_part)
channels.add_function(bot_quit)
channels.add_function(check_channel_members)
#channels.add_function(bot_connect)
#channels.add_function(bot_disconnect)
#channels.add_function(unauthorised_connect)
#channels.add_function(unauthorised_disconnect)
#channels.add_function(activity_report)
#channels.add_function(user_report)
channels.add_timer("channelcheck",hours=1)
