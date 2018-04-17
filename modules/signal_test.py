import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module

@module.command("signal",1,0)
@module.admin
def signal_fn(bot,message,regex_matches=None):
	sname = line.rest.split(" ",1)[1]
	signal(sname).send(None,bot=bot,line=line)

signal_test = module.Module("signal_test")
signal_test.add_function(signal_fn)
