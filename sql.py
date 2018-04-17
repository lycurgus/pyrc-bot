#!/usr/bin/env python3

import os
import sqlite3

def get_db(DBFILE='snuggles.sqlite'):
	if not os.path.exists(DBFILE):
		open(DBFILE,'w').close()
	db = sqlite3.connect(DBFILE)
	c = db.cursor()
	n = c.execute("SELECT count(*) FROM sqlite_master WHERE type='table';").fetchone()[0]
	if not (n > 1):
		with open('schema.sql') as s:
			c.executescript(s.read())
			db.commit()

get_db('snuggles.sqlite')
