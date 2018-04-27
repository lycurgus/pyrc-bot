import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random

@module.type("PRIVMSG")
@module.regex(r"^a+w+oo+!*$")
@module.timeout("howl")
def howl_fn(bot,message,regex_matches=None):
	if not bot.getcustom("asleep"):
		a = "a" * random.randint(1,3)
		w = "w" * random.randint(2,4)
		o = "o" * random.randint(4,7)
		#e = random.choices(["","!","!!","!!!"],weights=[40,30,20,10]) #not until python 3.6
		e = random.choice([val for val, cnt in [("",4),("!",3),("!!",2),("!!!",1)] for i in range(cnt)])
		howl = "{}{}{}{}".format(a,w,o,e)
		bot.commands.privmsg(message.replyto,howl)
	else:
		act = random.choice(["peeps in her sleep","sleepily mutters 'gonna start a howl...'"])
		bot.commands.action(message.replyto,act)

howl = module.Module("howl")
howl.add_function(howl_fn)
howl.add_timeout("howl",seconds=30)
