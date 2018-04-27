import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
# http://gitpython.readthedocs.io/en/stable/tutorial.html

@module.type("PRIVMSG")
@module.disable
@module.regex(r"^git pull$")
def git_pull(bot,message,regex_matches=None):
	bot.commands.privmsg(message.replyto,"pulling! (but not really, this is a stub)")

git = module.Module("git")
git.add_function(git_pull)
