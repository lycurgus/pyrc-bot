import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import time
import random

def get_ctcp(ctcp_type):
	ctcp_responses = {
		"TIME": ctcp_time,
		"VERSION": ctcp_version,
		"USERINFO": ctcp_userinfo,
		"WHOS-A-GOOD-BOY": ctcp_whos_a_good_boy,
		"SOURCE": ctcp_source,
		"PING": ctcp_ping
	}
	def ctcp_clientinfo():
		return " ".join([k for k,v in ctcp_responses.items()])
	def ctcp_unknown():
		return "huh?"
	ctcp_responses["CLIENTINFO"] = ctcp_clientinfo
	return ctcp_responses.get(ctcp_type,ctcp_unknown)()

def ctcp_ping():
	return time.strftime("%Y-%m-%d %H:%M:%S.%f")

def ctcp_time():
	return "time to get a watch! just kidding - it's {}".format(time.strftime("%c"))

def ctcp_version():
	return "bot:v0.5:linux x86_64"

def ctcp_userinfo():
	return "I'm a bot, beep boop."

def ctcp_whos_a_good_boy():
	return "Whoah, that's a hell of a question. http://www.threepanelsoul.com/comic/dog-philosophy"

def ctcp_source():
	responses = [
			"If you want to see my source code you'll have to buy me a drink first ;)",
			"just send me 'dcc' in PM, and i'll send you the files :)"
		]
	return random.choice(responses)

@module.ctcp
@module.regex(r"([\S]*)")
def resp_ctcp(bot,message,regex_matches=None):
	ctcp_type = regex_matches.group(1)
	if ctcp_type == "ACTION":
		return
	reply = get_ctcp(ctcp_type)
	bot.commands.ctcp_reply(message.sender,ctcp_type,reply)

ctcp = module.Module("ctcp")
ctcp.add_function(resp_ctcp)
