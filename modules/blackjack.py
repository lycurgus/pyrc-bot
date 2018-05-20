import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import re

class Blackjack:
	deal = "gb bj {}"
	hit = "gb hit"
	stay = "gb stay"
	wallet = "gb wallet"
	card_pattern = re.compile(r"(\d{1,2}|A|J|Q|K)\ ?(♠|♥|♦|♣)")
	colour_pattern = re.compile(r"\x03\d{2}(?:,\d{2})?")
	colour_reset = re.compile(r"\x0f")
	# Goatbot draws 9♠ [] for himself
	# Goatbot draws 2♦ for Silver
	# Goatbot draws 6♦ for Silver, who now has a score of 21!
	line_draws = re.compile(r".*draws (?P<cards>.*) for (?P<player>\w+).*")
	# Goatbot takes $20.00 from Silver and draws A♥ K♥ Silver gets Blackjack!
	# Goatbot takes $100.00 from SnuggleBunny and draws 2 ♠ 3 ♥
	line_deals = re.compile(r".*takes \$.* from (?P<player>\w+) and draws (?P<cards>.*).*")
	# SnuggleBunny has 4 ♥ 2 ♦ 3 ♦ J ♠, Goatbot has 5 ♦ === ##hand
	line_hands = re.compile(r".*(?P<player>\w+) has (?P<cards>.*), Goatbot has (?P<dealercards>.*).*")
	lines = (line_draws,line_deals,line_hands)
	def __init__(self):
		self.playing = False
		self.seen_hands = {}
		self.player_scores = {}
		self.wallet = 0.0

	def get_action(self,nick,amount=5):#TODO get a real amount somehow
		if not nick in self.seen_hands.keys() and not self.playing:
			return Blackjack.deal.format(amount)
		if self.playing:
			if self.seen_hands[nick] > 18:
				return Blackjack.hit
			else:
				return Blackjack.stay

	def check_funds(self):
		return "gb wallet" #TODO send this...

	def parse_hand(self,line):
		#self.playing = True
		#print(repr(line))
		no_colours = Blackjack.colour_reset.sub("",Blackjack.colour_pattern.sub("",line))
		if not any([suit in line for suit in ("♠","♥","♦","♣")]):
			return
		print(repr(no_colours))
		for linetype in Blackjack.lines:
			match = linetype.match(no_colours)
			if not match:
				continue
			p = match.group('player')
			if p == "himself":
				p = "Goatbot"
			h = match.group('cards')
			if 'dealercards' in match.groupdict().keys():
				d = match.group('dealercards')
			else:
				d = ""
			cards = re.findall(Blackjack.card_pattern,h)
			if not p in self.seen_hands.keys():
				self.seen_hands[p] = []
			self.seen_hands[p] += cards
			self.player_scores[p] = self.score_hand(self.seen_hands[p])
			print("player {} has score {}".format(p,self.player_scores[p]))

	def score_hand(self,cards):
		originals = [card[0] for card in cards] #cards are value,suit pairs
		values = [10 if val in ("J","Q","K") else val for val in originals]
		print(values)
		score = 0
		accum = 0
		aces = 0
		for card in values:
			if card == "A":
				aces += 1
			else:
				accum += int(card)
		while aces:
			accum += 1
			if accum > 12:
				accum += 10
			aces -= 1
		if accum < 22:
			if accum > score:
				score = accum
		else:
			score = 0
		return score

	def clear_game(self):
		self.playing = False
		self.seen_hands = {}
		self.player_scores = {}

@module.regex(r"_BOTNAMES_,?:?\ ?(?:what(?:'| i)s my score\??|bj score)",re.IGNORECASE)
def get_score(bot,message,regex_matches=None):
	if not message.channel:
		bot.commands.privmsg(message.replyto,"need to be in a channel..!")
	b = bot.getcustom('blackjack_{}'.format(message.channel))
	if not b:
		bot.commands.privmsg(message.replyto,"no game in progress..!")
		return
	if message.sender in b.player_scores.keys():
		c = len(b.seen_hands[message.sender])
		s = b.player_scores[message.sender]
		blackjack = (c ==2 and s == 21)
		if not bot.getcustom("asleep"):
			if blackjack:
				bot.commands.privmsg(message.replyto,"you have blackjack, {}".format(message.sender))
			else:
				bot.commands.privmsg(message.replyto,"you have {}, {}".format(s,message.sender))
		else:
			if blackjack:
				bot.commands.privmsg(message.replyto,"blackjack.")
			else:
				bot.commands.privmsg(message.replyto,"{}".format(b.player_scores[message.sender]))
	else:
		bot.commands.privmsg(message.replyto,"you're not playing, {}".format(message.sender))


@module.type("PRIVMSG")
@module.sender(["goatbot"])
#@module.regex(r"(\d{1,2}|\A|\J|\Q|\K)\ ?(♠|♥|♦|♣)")
def handle_game(bot,message,regex_matches=None):
	b = bot.getcustom('blackjack_{}'.format(message.channel))
	if not b:
		b = Blackjack()
		bot.setcustom('blackjack_{}'.format(message.channel),b)
	b.parse_hand(message.message)
	#bot.commands.privmsg(message.replyto,b.get_action(bot.nick))
	if any([winmsg in message.message for winmsg in ("A Tie.","claiming the bet","is paid out","is returned to")]):
		#lycurgus has [9 ♣] [4 ♠] [9 ♦]; Busted. A Tie. $20.00 is returned to lycurgus.
		#lycurgus has [5 ♦] [7 ♠] [3 ♥] [K ♠]; Busted. Goatbot wins, claiming the bet of $30.00 from lycurgus.
		#Vivacia has [5 ♥] [9 ♥] [2 ♥]; A score of 16, beating Goatbot. $32.35 is paid out to Vivacia.
		b.clear_game()

blackjack = module.Module("blackjack")
blackjack.add_function(handle_game)
blackjack.add_function(get_score)
