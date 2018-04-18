import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util

guess_pattern = r".*here you go:(?: _){{{}}}$"

@module.type("PRIVMSG")
@module.regex(guess_pattern.format(5))
@module.sender("taiya")
def guess_bunny(bot,message,regex_matches=None):
	if util.chance(0.9) or bot.getcustom("asleep"):
		return
	bot.commands.privmsg(message.replyto,"guess: bunny")

@module.type("PRIVMSG")
@module.regex(guess_pattern.format(6))
@module.sender("taiya")
def guess_rabbit(bot,message,regex_matches=None):
	if util.chance(0.9) or bot.getcustom("asleep"):
		return
	bot.commands.privmsg(message.replyto,"guess: rabbit")

guess = module.Module("guess")
guess.add_function(guess_bunny)
guess.add_function(guess_rabbit)
