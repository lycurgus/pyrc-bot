import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
from blinker import signal

@module.regex("^signal (.*)")
@module.admin
def signal_fn(bot,message,regex_matches=None):
	sname = regex_matches.group(1)
	signal(sname).send(None,bot=bot,line=message)

signal_test = module.Module("signal_test")
signal_test.add_function(signal_fn)
