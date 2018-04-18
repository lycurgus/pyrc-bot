import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.regex(r"^bada bing$")
@module.timeout("badabing")
@module.type("PRIVMSG")
def badaboom(bot,message,regex_matches=None):
	if bot.getcustom("asleep"):
		if util.chance(0.2):
			bot.commands.privmsg(message.replyto,"mumbles 'big bad-a boom' in her sleep")
		return
	bot.commands.privmsg(message.replyto,"bada boom")

badabing = module.Module("badabing")
badabing.add_function(badaboom)
badabing.add_timeout("badabing",seconds=45)
