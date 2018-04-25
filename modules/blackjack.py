import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import module
import re

class Blackjack:
	deal = "gb bj {}"
	hit = "gb hit"
	stay = "gb stay"
	wallet = "gb wallet"
	card_pattern = re.compile(r"(\d{1,2})\ ?(♠|♥|♦|♣)")
	colour_pattern = re.compile(r"\x03\d{2}(?:,\d{2})?")
	colour_reset = re.compile(r"\x0f")
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
		no_colours = Blackjack.colour_reset.sub(Blackjack.colour_pattern.sub(line))
		print(repr(no_colours))
		# Goatbot draws 9♠ [] for himself
		# Goatbot draws 2♦ for Silver
		# Goatbot draws 6♦ for Silver, who now has a score of 21!
		# (\d{1,2})\ ?(♠|♥|♦|♣)
		# Goatbot flips over 9♠ Q♥. Goatbot has 19
		# Goatbot flips over A♣ 5♦ and then draws 0♠ 5♣. Goatbot has 21
		# Goatbot takes $20.00 from Silver and draws A♥ K♥ Silver gets Blackjack!
		# Goatbot takes $100.00 from SnuggleBunny and draws 2 ♠ 3 ♥
		# (\d{1,2})\ ?(♠|♥|♦|♣)
		# SnuggleBunny has 4 ♥ 2 ♦ 3 ♦ J ♠, Goatbot has 5 ♦ ===
		# bot.name has (.*),.*   and then
		# (\d{1,2})\ ?(♠|♥|♦|♣)
		matches = re.findall(Blackjack.card_pattern,no_colours)
		print(matches)

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
	print(repr(message.message))
	no_starts = Blackjack.colour_pattern.sub("",message.message)
	no_colours = Blackjack.colour_reset.sub("",no_starts)
	print(repr(no_colours))
	matches = re.findall(Blackjack.card_pattern,no_colours)
	print("found cards: {}".format(matches))

blackjack = module.Module("blackjack")
blackjack.add_function(handle_game)
blackjack.setup_function = blackjack_setup
