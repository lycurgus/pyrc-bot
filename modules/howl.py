import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import random

@module.type("PRIVMSG")
@module.regex(r"^a+w+oo+!*$")
@module.timeout("howl")
def howl_fn(bot,message,regex_matches=None):
	if bot.awake:
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
