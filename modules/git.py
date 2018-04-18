import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.type("PRIVMSG")
@module.regex(r"^git pull$")
def git_pull(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"pulling! (but not really, this is a stub)")

git = module.Module("git")
git.add_function(git_pull)
