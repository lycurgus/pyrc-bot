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
	line_deals = re.compile(r".*takes $.* from (?P<player>\w+) and draws (?P<cards>.*).*")
	# SnuggleBunny has 4 ♥ 2 ♦ 3 ♦ J ♠, Goatbot has 5 ♦ === ##hand
	line_hands = re.compile(r".*(?P<player>\w+) has (?P<cards>.*), Goatbot has (?P,<dealercards>.*).*")
	lines = (line_draws,line_deals,line_hands)
	def __init__(self):
		self.score = 0
		self.seen_hands = {}

	def get_action(self):
		if self.score > 18:
			return Blackjack.hit
		else:
			return Blackjack.stay

	def deal_in(self,amount):
		return Blackjack.deal.format(amount)

	def parse_hand(self,line):
		#print(repr(line))
		no_colours = Blackjack.colour_reset.sub("",Blackjack.colour_pattern.sub("",line))
		print(repr(no_colours))
		if "himself" in line:
			return #goat's line
		if not any([suit in line for suit in ("♠","♥","♦","♣")]):
			return
		matches = re.findall(Blackjack.card_pattern,no_colours)
		print(matches)
		print("found cards totalling {}".format(self.score_hand(matches)))

	def score_hand(self,cards):
		originals = [card[0] for card in cards] #cards are value,suit pairs
		values = [val for val in originals if val not in ("J","Q","K")]
		while len(values) < len(originals):
			values.append(10)
		aces = [i for i,x in enumerate(values) if x == "A"]
		values = [int(x) for x in values if x != "A"]
		score = 0
		print(values)
		if aces == []:
			score = sum(values)
		else:
			possible_scores = []
			for a in aces:
				high = sum(values[:a]) + 11 + sum(values[a+1:])
				low = sum(values[:a]) + 1 + sum(values[a+1:])
				if high < 21:
					possible_scores.append(high)
				else:
					if low < 21:
						possible_scores.append(low)
			score = max(possible_scores)
		return score

	def _finish(self):
		self.bot.removecustom('blackjack')

	def finish_game(self,bot):
		self.bot = bot
		bot.queue_action(5,self._finish)


def blackjack_setup(bot):
	bot.setcustom('blackjack',Blackjack())

@module.type("PRIVMSG")
@module.sender(["goatbot"])
#@module.regex(r"(\d{1}|\A|\J|\Q|\K)\ ?(♠|♥|♦|♣)")
def handle_game(bot,message,regex_matches=None):
	b = bot.getcustom('blackjack')
	b.parse_hand(message.message)

blackjack = module.Module("blackjack")
blackjack.add_function(handle_game)
blackjack.setup_function = blackjack_setup
