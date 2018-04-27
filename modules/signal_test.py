import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module

@module.command("signal",1,0)
@module.admin
def signal_fn(bot,message,regex_matches=None):
	sname = line.rest.split(" ",1)[1]
	signal(sname).send(None,bot=bot,line=line)

signal_test = module.Module("signal_test")
signal_test.add_function(signal_fn)
