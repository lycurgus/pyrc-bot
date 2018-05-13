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
		print(repr(no_colours))
		if not any([suit in line for suit in ("♠","♥","♦","♣")]):
			return
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
				self.seen_hands[p] = 0
			self.seen_hands[p] += self.score_hand(cards)
			print("player {} has score {}".format(p,self.seen_hands[p]))

	def score_hand(self,cards):
		BUST = 22
		originals = [card[0] for card in cards] #cards are value,suit pairs
		values = [val for val in originals if val not in ("J","Q","K")]
		while len(values) < len(originals):
			values.append(10)
		print(values)
		aces = [i for i,x in enumerate(values) if x == "A"]
		values = [int(x) for x in values if x != "A"]
		score = 0
		if aces == []:
			score = sum(values)
		else:
			possible_scores = []
			for a in aces:
				high = sum(values[:a]) + 11 + sum(values[a+1:])
				low = sum(values[:a]) + 1 + sum(values[a+1:])
				if high < BUST:
					possible_scores.append(high)
				else:
					if low < BUST:
						possible_scores.append(low)
			score = max(possible_scores)
		return score

	def clear_game(self):
		self.playing = False
		self.seen_hands = {}


@module.type("PRIVMSG")
@module.sender(["goatbot"])
#@module.regex(r"(\d{1,2}|\A|\J|\Q|\K)\ ?(♠|♥|♦|♣)")
def handle_game(bot,message,regex_matches=None):
	b = bot.getcustom('blackjack')
	b.parse_hand(message.message)
	#bot.commands.privmsg(message.replyto,b.get_action(bot.nick))
	if any([winmsg in message.message for winmsg in ("A Tie.","claiming the bet","is paid out","is returned to")]):
		#lycurgus has [9 ♣] [4 ♠] [9 ♦]; Busted. A Tie. $20.00 is returned to lycurgus.
		#lycurgus has [5 ♦] [7 ♠] [3 ♥] [K ♠]; Busted. Goatbot wins, claiming the bet of $30.00 from lycurgus.
		#Vivacia has [5 ♥] [9 ♥] [2 ♥]; A score of 16, beating Goatbot. $32.35 is paid out to Vivacia.
		b.clear_game()

def blackjack_setup(bot):
	bot.setcustom('blackjack',Blackjack())

blackjack = module.Module("blackjack")
blackjack.add_function(handle_game)
blackjack.setup_function = blackjack_setup
