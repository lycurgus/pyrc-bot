import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta
import util
import re
from util import get_replyto

reminder_pattern = re.compile(r"^remind me ((?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?): (?P<message>.*)")

@module.user_not_present("taiya")
@module.regex(r"taiya,? (?:please )? tell (.*)")
def taiyas_not_here_man(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"taiya's not here, man")

@module.type("PRIVMSG")
@module.regex(r"remind me (.*): (.*)",re.IGNORECASE)
def remind_me(bot,message,regex_matches=None):
	#TODO store into sqlite??
	#TODO add a way for the person later speaking to trigger the reminder
	bot = kwargs['bot']
	line = kwargs['line']
	replyto = get_replyto(bot,line)
	reminder = reminder_pattern.match(line.rest)
	if reminder and False:
		#TODO needs a Reminder class, i think! Expectation is the reverse case...
		days = reminder.group('days')
		days = int(days) if days else 0
		hours = reminder.group('hours')
		hours = int(hours) if hours else 0
		minutes = reminder.group('minutes')
		minutes = int(minutes) if minutes else 0
		message = reminder.group('message')
		c = {
				'nick': line.nick,
				'type': 'PRIVMSG'
			}
		ea = [bot.commands.privmsg]
		ep = [[line.nick,"you wanted me to remind you: {}".format(message)]]
		d = timedelta(days=days,hours=hours,minutes=minutes)
		bot.expectations.append(util.Expectation(bot,c,[],[[]],d,ea,ep))
		if not bot.getcustom("asleep"):
			bot.commands.privmsg(replyto,"ok! i'll try not to forget :)")
		else:
			bot.commands.action(replyto,"nods sleepily at {}".format(line.nick))

remind = module.Module("remind")
remind.add_function(remind_me)
