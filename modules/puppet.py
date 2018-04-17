import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import timedelta


@module.type("PRIVMSG")
@module.admin
@module.regex(r'^say (?P<target>.*): (?P<line>.*)$')
def line_puppet(bot,message,regex_matches=None):
	target = regex_matches.group('target')
	line = regex_matches.group('line')
	bot.commands.privmsg(target,line)

@module.type("PRIVMSG")
@module.admin
@module.regex(r'^act (?P<target>.*): (?P<action>.*)$')
def act_puppet(bot,message,regex_matches=None):
	target = regex_matches.group('target')
	action = regex_matches.group('action')
	bot.commands.action(target,action)

puppet = module.Module("puppet")
puppet.add_function(line_puppet)
puppet.add_function(act_puppet)
