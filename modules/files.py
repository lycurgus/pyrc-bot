import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
from datetime import datetime
import glob
import os
import time
import re
import socket
from IGD import addPortMapping, delPortMapping, getExternalIpAddress

def decode_ip_addr(address_int):
	"""decodes a 32-bit int into IP octets (for DCC use)"""
	ip_octets = []
	if((address_int > 0xffffffff) or (address_int < 0)):
		ip_octets = ["0","0","0","0"]
	else:
		ip_octets.append(str((address_int & 0xff000000) >> 24))
		ip_octets.append(str((address_int & 0x00ff0000) >> 16))
		ip_octets.append(str((address_int & 0x0000ff00) >> 8))
		ip_octets.append(str((address_int & 0x000000ff)))
	return ".".join(ip_octets)

def encode_ip_addr(address_octets):
	"""encodes IP octets into a 32-bit int (for DCC use)"""
	ip_int = 0
	octets = address_octets.split('.')
	if(len(octets) == 4):
		ip_int += int(octets[0]) << 24
		ip_int += int(octets[1]) << 16
		ip_int += int(octets[2]) << 8
		ip_int += int(octets[3])
	return str(ip_int)

def split_message(message):
	"""generator returning chunks of a too-long message"""
	while message:
		s = message[360:400].find(' ')
		split = 380 if s == -1 else s+360
		yield message[:split]
		message = message[split:].strip()

def get_public_ip():
	ip = getExternalIpAddress()
	if not ip: #if we can't find an IGD device, just hit the webservice
		import urllib.request
		with urllib.request.urlopen("http://ifconfigme.herokuapp.com") as response:
			contents = response.read()
		ip = contents.decode('UTF-8')
	print("checked my ip: it's {}".format(ip))
	return ip

def get_local_ip():
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.connect(("8.8.8.8",80))
	return s.getsockname()[0]

def get_free_port():
	"""get a free port on localhost to use for DCC"""
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('localhost',0))
	a, p = s.getsockname()
	s.close()
	return str(p)

def package_source(extensions,subdirectories=[]):
	if isinstance(extensions,str):
		extensions = [extensions]
	if isinstance(subdirectories,str):
		subdirectories = [subdirectories]
	subdirectories.insert(0,".")
	import os
	import string
	import random
	import tarfile
	import glob
	filename =  ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)) + '.tar.gz'
	while True:
		try:
			tar = tarfile.open(filename,"w:gz")
		except tarfile.TarError:
			filename =  ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)) + '.tar'
			continue
		break
	print("dcc: using tar file {}".format(filename))
	for subdirectory in subdirectories:
		for extension in extensions:
			extension = extension.lstrip("*.")
			for foundfile in glob.glob("{}/*.{}".format(subdirectory,extension)):
				print("dcc: adding file {} to tar".format(foundfile))
				tar.add(foundfile)
	tar.close()
	filesize = os.stat(filename).st_size
	print("dcc: file {} is {} bytes in size".format(filename,filesize))
	return filename, filesize

def dcc_get_socket_for(filename,port):
	import threading
	t = threading.Thread(target=_dcc_get_socket_for,daemon=True,kwargs={'filename':filename,'port':port})
	t.start()

def _dcc_get_socket_for(filename,port):
	import os
	myip = get_local_ip()
	print('got ip ({})'.format(myip))
	chk = addPortMapping(myip,port) #punch hole in firewall
	print('firewall hole punched for port {}: {}'.format(port,chk))
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('',int(port)))
	s.listen(1)
	s.settimeout(60)
	print('listening for DCC connection')
	try:
		conn, addr = s.accept() #blocks
	except socket.timeout:
		print('DCC listen timed out!')
	else:
		s.close()
		print('DCC connection established from {}'.format(addr))
		print('sending file {} by DCC to client at {}'.format(filename,addr))
		filesize = os.stat(filename).st_size
		conn.setblocking(1)
		with open(filename,"r") as data:
			conn.send(bytearray(data.read().encode()))
			print('data sent, doing recv')
			r = conn.recv(1024)
			print('got {} back and it was {}'.format(len(r),repr(r)))
			print('recv done, closing')
		conn.close()
	finally:
		print('removing {}'.format(filename))
		os.remove(filename)

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
#!/usr/bin/env python3

