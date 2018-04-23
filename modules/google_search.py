import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from search import Google

@module.user_not_present("taiya")
@module.type("PRIVMSG")
@module.regex(r"^g (.*)$")
def googlesearch(bot,message,regex_matches=None):
	query = regex_matches.group(1)
	result = Google.search(query)
	bot.commands.privmsg(message.replyto,result,True)

google_search = module.Module("google_search")
google_search.add_function(googlesearch)
