import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import util
import re

@module.type("PRIVMSG")
@module.regex(r"!np(?: (yt|sc))?")
def nowplaying_fn(bot,message,regex_matches=None):
	import socket
	import ssl
	from lxml import etree
	from hashlib import md5
	from util import random_characters
	#from urllib.parse import quote_plus
	if not bot.awake:
		if util.chance(0.5):
			return
	yt = regex_matches.group(1) == "yt"
	sc = regex_matches.group(1) == "sc"
	host = "s.lycr.gs"
	port = 443
	path = "rest/getNowPlaying"
	auth_user = "snugglebunny"
	auth_pass = "carrot5"
	auth_salt = random_characters(10)
	auth_tokn = md5("{}{}".format(auth_pass,auth_salt).encode("UTF-8")).hexdigest()
	querystring = "u={u}&t={t}&s={s}&v={v}&c={c}".format(u=auth_user,t=auth_tokn,s=auth_salt,v="1.15",c="snugglebunny")
	resource = "{}?{}".format(path,querystring)
	request = "GET /{} HTTP/1.1\r\nhost: {}\r\n\r\n".format(resource,host).encode("UTF-8")
	s = ssl.wrap_socket(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
	s.connect((host,port))
	s.send(request)
	resp = "".encode("UTF-8")
	while True:
		rcv = s.recv(2048)
		if not rcv:
			break
		resp += rcv
	s.close()
	xml = resp.decode("UTF-8").split("\r\n\r\n")[1].strip()
	xml = xml.replace(' encoding="UTF-8"','')
	xml = xml.replace('\n','')
	#print(xml)
	root = etree.fromstring(xml)
	entries = root.findall(".//{http://subsonic.org/restapi}entry")
	if len(entries) == 1:
		entry = entries[0]
		artist = entry.attrib['artist']
		track = entry.attrib['title']
		if yt:
			if util.find_on_server(bot,"taiya"):
				c = {
						"nick": "taiya",
						"type": "PRIVMSG"
					}
				a = [bot.commands.privmsg]
				p = [[message.replyto,[re.compile(r"(.*)"),1],True]]
				e = timedelta(seconds=15)
				ea = [bot.commands.privmsg]
				ep = [[message.replyto,"taiya didn't help me look up the link :("]]
				bot.expectations.append(Expectation(c,a,p,e,ea,ep))
				bot.commands.privmsg("taiya","yt {} {}".format(artist,track),True)
			else:
				bot.commands.privmsg(message.replyto,"taiya's not around to look it up for me!",True)
				bot.commands.privmsg(message.replyto,"the track is {} by {}, though".format(track,artist))
			#bot.commands.privmsg(message.replyto,"yt {} {}".format(artist,track),True)
		elif sc:
			if util.find_on_server(bot,"taiya"):
				c = {
						"nick": "taiya",
						"type": "PRIVMSG"
					}
				a = [bot.commands.privmsg]
				p = [[message.replyto,[re.compile(r"(.*)"),1],True]]
				e = timedelta(seconds=15)
				ea = [bot.commands.privmsg]
				ep = [[message.replyto,"taiya didn't help me look up the link :("]]
				bot.expectations.append(Expectation(c,a,p,e,ea,ep))
				bot.commands.privmsg("taiya","yt {} {}".format(artist,track),True)
			else:
				bot.commands.privmsg(message.replyto,"taiya's not around to look it up for me!",True)
				bot.commands.privmsg(message.replyto,"the track is {} by {}, though".format(track,artist))
			#bot.commands.privmsg(message.replyto,"g soundcloud {} {}".format(artist,track),True)
		else:
			bot.commands.privmsg(message.replyto,"now playing: {} - {}".format(artist,track),True)
	elif len(entries) > 1:
		bot.commands.privmsg(message.replyto,"now playing:",True)
		for entry in entries:
			artist = entry.attrib['artist']
			track = entry.attrib['title']
			user = entry.attrib['username']
			player = entry.attrib['playerId']
			bot.commands.privmsg(message.replyto,"{} - {} ({}@{})".format(artist,track,user,player),True)
	else:
		bot.commands.privmsg(message.replyto,"nothing playing right now!",True)

nowplaying = module.Module("nowplaying")
nowplaying.add_function(nowplaying_fn)
