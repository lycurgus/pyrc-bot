import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module

@module.admin
@module.direct
@module.type("PRIVMSG")
@module.regex(r'.*\sload\s+([^\s]*)')
def load_module(bot,message,regex_matches=None):
	module_name = regex_matches.group(1)
	try:
		bot.load_module(module_name)
	except:
		bot.commands.privmsg(message.replyto,"{}something went wrong!".format("" if message.parameters[0] == bot.nick else "{}: ".format(message.sender)))
	else:
		bot.commands.privmsg(message.replyto,"{}done!".format("" if message.parameters[0] == bot.nick else "{}: ".format(message.sender)))

@module.admin
@module.direct
@module.type("PRIVMSG")
@module.regex(r'.*\sreload\s+([^\s]*)$')
def reload_module(bot,message,regex_matches=None):
	module_name = regex_matches.group(1)
	if module_name == "all":
		bot.reload_all_modules()
	else:
		try:
			bot.reload_module(module_name)
		except:
			bot.commands.privmsg(message.replyto,"{}something went wrong!".format("" if message.parameters[0] == bot.nick else "{}: ".format(message.sender)))
		else:
			bot.commands.privmsg(message.replyto,"{}done!".format("" if message.parameters[0] == bot.nick else "{}: ".format(message.sender)))

@module.admin
@module.direct
@module.type("PRIVMSG")
@module.regex(r'.*\sunload\s+([^\s]*)$')
def unload_module(bot,message,regex_matches=None):
	module_name = regex_matches.group(1)
	if module_name == "all":
		bot.unload_all_modules()
	else:
		bot.unload_module(module_name)

reloader = module.Module("reloader")
reloader.add_function(load_module)
reloader.add_function(reload_module)
reloader.add_function(unload_module)
