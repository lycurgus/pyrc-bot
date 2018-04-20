import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.regex(r"(?:maximum )?rabbit")
@module.type("PRIVMSG")
def max_rabbit(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"ᴍᴀxɪᴍᴜᴍ ʀᴀʙʙɪᴛ")

maximum = module.Module("maximum")
maximum.add_function(max_rabbit)
