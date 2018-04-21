#!/usr/bin/env python3

from asyncio import get_event_loop#, gather
import sqlite3
import socket
from threading import Thread
from time import sleep
from blinker import signal
from connections import Supervisor

def get_servers():
	db = sqlite3.connect('snuggles.sqlite')
	c = db.cursor()
	c.row_factory = sqlite3.Row
	s = c.execute("SELECT name,host,port FROM servers WHERE enabled = 1").fetchall()
	servers = []
	for server in s:
		servers.append({
			'name': server['name'],
			'host': server['host'],
			'port': server['port']
			})
	return servers

class Metronome:
	delta = { "d": 0.25 }
	base = signal("TICK-base")
	def __init__(self):
		self.active = True
		def stop(sender,**kwargs):
			self.active = False
		self.stop = stop
		signal("TICK-stop").connect(self.stop)
		def start(sender=None,**kwargs):
			self.active = True
			Thread(target=self.run,daemon=True).start()
		self.start = start
		signal("TICK-start").connect(self.start)

	def run(self):
		while self.active:
			Metronome.base.send(None,**Metronome.delta)
			sleep(Metronome.delta["d"])

if __name__ == "__main__":
	sup = Supervisor(get_event_loop())
	for s in get_servers():
		sup.connect(s)

	m = Metronome()
	m.start()

	#tasks = [connection.task for key,connection in sup.connections.items()]
	try:
		sup.loop.run_forever()
		#sup.loop.run_until_complete(gather(*tasks)) #exits when task(s) done though
	except KeyboardInterrupt:
		sup.loop.stop()
		print("\nShutting down...")
	finally:
		sup.loop.close()
