import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from ddate.base import DDate
from datetime import datetime
from datetime import timedelta
from time import time

def disco_time():
	#THUD is 5 THUD minutes long = 115 real minutes
	#one THUD minute = 23 THUD seconds = 23 real minutes (1 THUD second = 1 real minute)
	#after THUD each hour = 5 minutes (real and discordian). 1 discordian second = 12 real seconds
	now = int(time())
	#print("now: {}".format(now))
	since_midnight = now % days(1)
	#print("seconds since midnight: {}".format(since_midnight))
	discordian_day_start = hours(5) + minutes(23)
	#print("day start is: {}".format(discordian_day_start))
	thud_length = minutes(115)
	#print("thud length is: {}".format(thud_length))
	discordian_timestamp = (since_midnight - discordian_day_start + hours(24)) % hours(24)
	#print("discordian_timestamp: {}".format(discordian_timestamp))
	thud_p = discordian_timestamp < thud_length
	if thud_p:
		hour = "THUD" #constant
		minute = (discordian_timestamp // minutes(23)) #0-4
		second = ((discordian_timestamp // 60)) % 23 #0-22
	else:
		post_thud_timestamp = discordian_timestamp - thud_length
		#print("time after THUD: {}".format(post_thud_timestamp))
		hour = (post_thud_timestamp // minutes(5)) #0-264
		minute = ((post_thud_timestamp - (hour * minutes(5))) // minutes(1)) #0-4
		second = ((post_thud_timestamp // 12) % 5) #0-4
	time_str = "it is {}:{}:{}".format(hour,minute,second)
	return time_str

@module.direct
@module.regex(r"what time is it\?")
def discord_time(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,disco_time())

@module.direct
@module.regex(r"what day is it\?")
def discord_date(bot,message,regex_matches=None):
	ddate = DDate(date=datetime.utcnow() + timedelta(hours=5) + timedelta(minutes=23))
	bot.commands.privmsg(message.replyto,"it's {}".format(str(ddate).replace("Today is ","")))

discordian = module.Module("discordian")
discordian.add_function(discord_time)
discordian.add_function(discord_date)
