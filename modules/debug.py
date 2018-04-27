import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module

@module.type("PRIVMSG")
@module.regex(r"check users (.*)")
def users_check(bot,message,regex_matches=None):
	channel = regex_matches.group(1).strip()
	if channel in bot.channels.keys():
		print(" ".join(bot.channels[channel].users.keys()))
		print("count: {}".format(len(bot.channels[channel].users.keys())))

@module.type("PRIVMSG")
@module.regex(r"is (.*) in (.*)")
def user_check(bot,message,regex_matches=None):
	user = regex_matches.group(1).strip()
	channel = regex_matches.group(2).strip()
	if channel in bot.channels.keys():
		print(True if user in bot.channels[channel].users.keys() else False)

debug = module.Module("debug")
debug.add_function(users_check)
debug.add_function(user_check)
