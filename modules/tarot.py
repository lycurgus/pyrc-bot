import sys
if not ".." in sys.path:
	sys.path.insert(0,"..")

import module
import random
from datetime import datetime
import re

class Deck:
	suits = ["Cups","Wands","Pentacles","Swords"]
	cards = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Page","Knight","Queen","King"]
	major = ["0 - The Fool","1 - The Magician","2 - The High Priestess","3 - The Empress","4 - The Emperor","5 - The Hierophant","6 - The Lovers","7 - The Chariot","8 - Strength","9 - The Hermit","10 - The Wheel of Fortune","11 - Justice","12 - The Hanged Man","13 - Death","14 - Temperance","15 - The Devil","16 - The Tower","17 - The Star","18 - The Moon","19 - The Sun","20 - Judgement","21 - The World"]
	def __init__(self):
		self.deck = {}
		self.build()

	def build(self):
		minor = []
		for suit in Deck.suits:
			for card in Deck.cards:
				minor.append("{} of {}".format(card,suit))
		self.deck = {n: c for n,c in enumerate(minor+Deck.major)}

	def draw(self):
		if len(self.deck) == 0:
			print("out of cards, new deck")
			self.build()
		num,card = random.choice(list(self.deck.items()))
		del self.deck[num]
		return card

	def draw_three(self):
		return (self.draw(), self.draw(), self.draw())

@module.type("PRIVMSG")
@module.regex(r"_BOTNAMES_:?,? read my tarot.*")
def tarot_fn(bot,message,regex_matches=None):
	today = datetime.today().strftime("%Y%m%d")
	user = message.sender
	still = " still"
	if not bot.getcustom("tarot_deck"):
		bot.setcustom("tarot_deck",Deck())
	if not bot.getcustom("tarot"):
		bot.setcustom("tarot",{})
	t = bot.getcustom("tarot")
	if not today in t.keys():
		t[today] = {}
	if not user in t[today].keys():
		still = ""
		t[today][user] = bot.getcustom("tarot_deck").draw_three()
	cards = re.sub(r"\d+\ \-\ ","",", ".join(t[today][user]))
	bot.commands.privmsg(message.replyto,"{}: your cards are{}: {}".format(message.sender,still,cards),True)

tarot = module.Module("tarot")
tarot.add_function(tarot_fn)
