import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from search import Google
from search import Youtube

@module.user_not_present("taiya")
@module.type("PRIVMSG")
@module.regex(r"^g (.*)$")
def googlesearch(bot,message,regex_matches=None):
	query = regex_matches.group(1)
	result = Google.search(query)
	bot.commands.privmsg(message.replyto,result,True)

@module.user_not_present("taiya")
@module.type("PRIVMSG")
@module.regex(r"^yt (.*)$")
def youtubesearch(bot,message,regex_matches=None):
	query = regex_matches.group(1)
	result = Youtube.search(query)
	bot.commands.privmsg(message.replyto,result,True)

@module.user_not_present("taiya")
@module.type("PRIVMSG")
@module.regex(r"^w (.*)$")
def wikipediasearch(bot,message,regex_matches=None):
	query = regex_matches.group(1)
	result = Google.search("wikipedia "+query)
	bot.commands.privmsg(message.replyto,result,True)

searches = module.Module("searches")
searches.add_function(googlesearch)
searches.add_function(youtubesearch)
searches.add_function(wikipediasearch)
