import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import rnr
from datetime import datetime
import glob
import os
import time

@module.regex(r"^\s*dcc\s*$")
@module.direct
@module.type("PRIVMSG")
def dcc(bot,message,regex_matches=None):
	print('got dcc request')
	bot.commands.privmsg(message.replyto,"ok, sending you a DCC, {}".format(message.sender))
	(filename,filesize) = rnr.package_source(["py"],["modules"])
	my_ip_int = rnr.encode_ip_addr(rnr.get_public_ip())
	port = rnr.get_free_port()
	bot.commands.dcc_offer(message.sender,filename,filesize,my_ip_int,port)
	rnr.dcc_get_socket_for(filename,port) #starts its own thread
	bot.commands.privmsg(bot.boss,"dcc requested by {}".format(message.sender))

@module.command("updated")
@module.type("PRIVMSG")
def updated(bot,message,regex_matches=None):
	updated_string, updated_ago = get_source_updated_string()
	bot.commands.privmsg(message.replyto,"my files were last updated {} ({} ago)".format(updated_string, updated_ago))

def get_source_updated_string():
	latest = 0
	for foundfile in glob.glob("*.py"):
		updated = os.path.getmtime(foundfile)
		if updated > latest:
			latest = updated
	updated_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(updated))
	updated_ago = "about"
	updated_diff = datetime.now() - datetime.fromtimestamp(updated)
	updated_days = updated_diff.days
	updated_hours = updated_diff.seconds // 3600
	if updated_days:
		updated_ago = updated_ago + "{} day".format(updated_days)
		if updated_days > 1:
			updated_ago = updated_ago + "s"
	if updated_days and updated_hours:
		updated_ago = updated_ago + " and "
	if updated_hours:
		updated_ago = updated_ago + " {} hour".format((updated_hours))
		if updated_hours > 1:
			updated_ago = updated_ago + "s"
	if not updated_days and not updated_hours:
			updated_ago = "not too long"
	return updated_string, updated_ago

@module.command("filecount")
@module.type("PRIVMSG")
def filecount(bot,message,regex_matches=None):
	import glob
	number = len(glob.glob("*.py"))
	modules = len(glob.glob("modules/*.py"))
	bot.commands.privmsg(message.replyto,"i am comprised of {} core files and {} modules".format(number,modules))
	bot.commands.privmsg(message.replyto,"(that number probably inaccurate due to refactoring!)")

files = module.Module("files")
files.add_function(dcc)
#files.add_function(updated)
#files.add_function(filecount)
