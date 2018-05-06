import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import util
from lxml import html
import urllib.request

@module.user_not_present("saoirse")
@module.type("PRIVMSG")
@module.regex(r".*linux.*")
@module.timer("yay_things")
def yay_linux(bot,message,regex_matches=None):
	if not bot.getcustom('asleep'):
		if util.chance(0.6):
			bot.commands.privmsg(message.replyto,"yay Linux!")

@module.user_not_present("saoirse")
@module.type("PRIVMSG")
@module.regex(r".*c\+\+.*")
@module.timer("yay_things")
def yay_cplusplus(bot,message,regex_matches=None):
	if not bot.getcustom('asleep'):
		if util.chance(0.6):
			bot.commands.privmsg(message.replyto,"yay C++!")

@module.user_not_present("saoirse")
@module.type("PRIVMSG")
@module.regex(r".*(?:windows|microsoft).*")
@module.timer("yay_things")
def curse_windows(bot,message,regex_matches=None):
	if not bot.getcustom('asleep'):
		if util.chance(0.6):
			bot.commands.action(message.replyto,"shakes fist at Microsoft")

@module.user_not_present("saoirse")
@module.sender_not(["taiya","mechataiya","narwhaltaiya"])
@module.type("PRIVMSG")
@module.regex(r".*(http(?:s)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+).*")
def page_title(bot,message,regex_matches=None):
	url = regex_matches.group(1)
	head = {'User-Agent': 'Chrome/35.0.1916.47'}
	reqs = urllib.request.Request(url,headers=head)
	resp = urllib.request.urlopen(reqs)
	if resp.headers.get_content_type() not in ("text/html"):
		print("got a header of {}".format(resp.headers.get_content_type()))
		return
	try:
		tree = html.fromstring(resp.read().decode('utf-8'))
	except UnicodeDecodeError:
		return
	title = tree.xpath('//title')[0].text.strip()
	bot.commands.privmsg(message.replyto,title,True)

@module.regex(r"^\!(?:eyebrows|lenny)$")
@module.user_not_present("saoirse")
def lenny(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"( ͡° ͜ʖ ͡°)")

saoirse = module.Module("saoirse")
saoirse.add_function(yay_linux)
saoirse.add_function(yay_cplusplus)
saoirse.add_function(curse_windows)
saoirse.add_function(page_title)
saoirse.add_function(lenny)
saoirse.add_timeout("yay_things",minutes=2)
