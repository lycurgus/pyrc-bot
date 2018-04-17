import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from ddate.base import DDate
from datetime import datetime
from datetime import timedelta

@module.direct
@module.regex(r"what time is it\?")
def discord_time(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,discord_time())

@module.direct
@module.regex(r"what day is it\?")
def discord_date(bot,message,regex_matches=None):
	ddate = DDate(date=datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=23))
	bot.commands.privmsg(message.replyto,"it's {}".format(str(ddate).replace("Today is ","")))

discordian = module.Module("discordian")
discordian.add_function(discord_time)
discordian.add_function(discord_date)
