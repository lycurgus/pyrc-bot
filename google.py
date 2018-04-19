#!/usr/bin/env python3

import urllib.request
import urllib.parse
import ssl
from lxml import html

def search(query):
	h = {
			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "en-us,en;q=0.5",
			"Cookie": _getcookies()
	}
	q = urllib.parse.urlencode({ "q": query },quote_via=urllib.parse.quote)
	u = "https://www.google.com/search?{}".format(q)
	rq = urllib.request.Request(u,headers=h)
	rs = urllib.request.urlopen(rq,context=ssl.create_default_context())
	text = rs.read()
	found = html.fromstring(text.decode('utf-8')).xpath('//div[@class="rc"]')[0]
	t = found.xpath('./h3/a')[0].text
	h = found.xpath('./h3/a')[0].get('href')
	return "{}: {}".format(t,h)

def _getcookies():
	rq = urllib.request.Request("https://www.google.com",method="HEAD")
	rs = urllib.request.urlopen(rq)
	c = ""
	first = True
	for hdr,val in rs.getheaders():
		if hdr.lower() == "set-cookie":
			if not first:
				c += "; "
			c += val.split(";",1)[0]
			first = False
	return c

if __name__ == "__main__":
	query = input("google search: ")
	print(search(query))
