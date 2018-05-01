from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Server(Base):
	__tablename__ = 'servers'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	host = Column(String(250), nullable=False)
	port = Column(Integer, nullable=False)
	enabled = Column(Boolean, nullable=False)
	post_connect = Column(string(500))

class Identity(Base):
	__tablename__ = 'identities'
	id = Column(Integer, primary_key=True)
	server_id = Column(Integer, ForeignKey('servers.id'))
	name = Column(String(250), nullable=False))
	boss = Column(String(250), nullable=False))
	bedtime = Column(Integer)
	waketime = Column(Integer)
	ns_pass = Column(String(50))

class NickName(Base):
	__tablename__ = 'nicknames'
	id = Column(Integer, primary_key=True)
	identity_id = Column(Integer, ForeignKey('identities.id'))
	name = Column(String(250), nullable=False))

class KnownUser(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	server_id = Column(Integer, ForeignKey('servers.id'))
	name = Column(String(250), nullable=False))

class UserAlt(Base):
	__tablename__ = 'user_alts'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	name = Column(String(250), nullable=False))



class BotStorage:
	def __init__(self):
		pass




"""
used:

identities
id• |serverId•  |nick•  •   •   |boss•  •   |bedtime•   |waketime•  |ns_pass
1•  |1• •   •   |SnuggleBunny•  |lycurgus•  |22••   •   |8• •   •   |
2•  |2• •   •   |SnuggleBun••   |slycurgus• |22••   •   |8• •   •   |

pet names
id• |identityId•|name
1•  |1• •   •   |snuggles
2•  |1• •   •   |bugglesnunny
3•  |1• •   •   |snugorobunneru
new: snoogles

servers
id• |name•  •   |host•  •   •   •   |port|enabled
1•  |gamesurge• |irc.gamesurge.net• |6667|1
2•  |freenode•  |irc.freenode.net•  |6667|0
"""
