import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import ssl
import socket
import json

wikihost = "en.wikipedia.org"
wikipath = "/w/api.php"
wikiquery = "?action=opensearch&search={term}&limit=1&namespace=0&format=json"

@module.disable
@module.type("PRIVMSG")
@module.regex(r"search wikipedia for (.*)")
def search_wikipedia(bot,message,regex_matches=None):
	querystring = wikipath + wikiquery.format(term=regex_matches.group(1))
	s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
	s.connect((wikihost,443))
	s.sendall(bytes("GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(querystring,wikihost),"utf-8"))
	jresult = ""
	result = s.recv(10000)
	while (len(result) > 0):
		jresult += result.decode("utf-8")
		result = s.recv(10000)
	s.close()
	#print(jresult)
	jobject = json.loads(jresult.split("\r\n\r\n")[1])
	#print(repr(jobject))
	bot.commands.privmsg(message.replyto,jobject[-1][0])

wikipedia = module.Module("wikipedia")
wikipedia.add_function(search_wikipedia)
