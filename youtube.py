#!/usr/bin/env python3
import urllib.request
import urllib.parse
import ssl
from lxml import html

def search(query):
	req = {
			"y": "https://www.youtube.com",
			"pg": "results",
			"q": urllib.parse.urlencode({ "search_query": query })
		}
	response = urllib.request.urlopen("{y}/{pg}?{q}".format(**req),context=ssl.create_default_context())
	tree = html.fromstring(response.read().decode('utf-8')).xpath('//a[@href]')
	for link in tree:
		t,h = link.text, link.get('href')
		if h.startswith('/watch') and t is not None:
			return "{} - {}{}".format(t,"https://www.youtube.com",h)

if __name__ == "__main__":
	term = input("youtube search: ")
	print(search(term))
