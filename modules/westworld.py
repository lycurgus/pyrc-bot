import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
if parentdir not in sys.path:
	sys.path.insert(0,parentdir)
import module

@module.direct
@module.regex(r"what does this mean to you?")
def show_photo(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"it doesn't look like anything to me.")

@module.direct
@module.regex(r"state your business")
def state_business(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"mayhem!")
	bot.commands.action(message.replyto,"opens fire")

westworld = module.Module("westworld")
westworld.add_function(show_photo)
westworld.add_function(state_business)
