import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import time

@module.regex(r"bug report: (.*)")
@module.direct
@module.type("PRIVMSG")
def report_bug(bot,message,regex_matches=None):
	with open("bugreports.txt","a") as bf:
		bf.write("{} - {}: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"),message.sender,regex_matches.group(1)))
	print("bug reported: {}".format(regex_matches.group(1)))

@module.regex(r"feature request: (.*)")
@module.direct
@module.type("PRIVMSG")
def request_feature(bot,message,regex_matches=None):
	with open("featurerequests.txt","a") as ff:
		ff.write("{} - {}: {}".format(time.strftime("%Y-%m-%d %H:%M:%S"),message.sender,regex_matches.group(1)))
	print("feature requested: {}".format(regex_matches.group(1)))

bugreport = module.Module("bugreport")
bugreport.add_function(report_bug)
bugreport.add_function(request_feature)
