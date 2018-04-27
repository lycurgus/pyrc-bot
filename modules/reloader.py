import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module

@module.admin
#@module.direct
@module.type("PRIVMSG")
@module.regex(r'^load\s+([^\s]*)$')
def load_module(bot,line,regex_matches=None):
	module_name = regex_matches.group(1)
	bot.load_module(module_name)

@module.admin
#@module.direct
@module.type("PRIVMSG")
@module.regex(r'^reload\s+([^\s]*)$')
def reload_module(bot,line,regex_matches=None):
	module_name = regex_matches.group(1)
	if module_name == "all":
		bot.reload_all_modules()
	else:
		bot.reload_module(module_name)

@module.admin
#@module.direct
@module.type("PRIVMSG")
@module.regex(r'^unload\s+([^\s]*)$')
def unload_module(bot,line,regex_matches=None):
	module_name = regex_matches.group(1)
	if module_name == "all":
		bot.unload_all_modules()
	else:
		bot.unload_module(module_name)

reloader = module.Module("reloader")
reloader.add_function(load_module)
reloader.add_function(reload_module)
reloader.add_function(unload_module)
