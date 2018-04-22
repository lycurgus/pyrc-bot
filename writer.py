import re

foreColours = {
		'black': '30',
		'dark_gray': '90', 'dark_grey': '90', 'gray': '90', 'grey': '90',
		'light_gray': '37', 'light_grey': '37',
		'white': '97',
		'dark_red': '31',
		'light_red': '91',
		'dark_green': '32',
		'light_green': '92',
		'orange': '33', 'dark_yellow': '33',
		'yellow': '93', 'light_yellow': '93',
		'dark_blue': '34',
		'light_blue': '94',
		'magenta': '35', 'dark_magenta': '35',
		'light_magenta': '95',
		'cyan': '36', 'dark_cyan': '36',
		'light_cyan': '96'
	}

backColours = {
		'black': '40',
		'dark_gray': '100', 'dark_grey': '100', 'gray': '100', 'grey': '100',
		'light_gray': '47', 'light_grey': '47',
		'white': '107',
		'dark_red': '41',
		'light_red': '101',
		'dark_green': '42',
		'light_green': '102',
		'orange': '43', 'dark_yellow': '43',
		'yellow': '103', 'light_yellow': '103',
		'dark_blue': '44',
		'light_blue': '104',
		'magenta': '45', 'dark_magenta': '45',
		'light_magenta': '105',
		'cyan': '46', 'dark_cyan': '46',
		'light_cyan': '106'
	}

def replace(message):
	message = re.sub(r"\$\{reset\}","\x1b[0m",message)
	message = re.sub(r"\$\{([_a-z]+)(?:\,([_a-z]+))?\s?(b|bold)?\s?(u|ul|under|line|underline)?\}",set_colours,message)
	message = re.sub(r"\$\{[a-z]+\}","",message)
	return message

def set_colours(match):
	fore = match.group(1) if match.group(1) else None
	back = match.group(2) if match.group(2) else None
	bold = True if match.group(3) else False
	undr = True if match.group(4) else False
	code = "\x1b"
	bits = []
	if bold:
		bits.append("1")
	else:
		bits.append("21")
	if undr:
		bits.append("24")
	else:
		bits.append("24")
	if fore in foreColours.keys():
		bits.append(foreColours[fore])
	else:
		bits.append("39")
	if back in backColours.keys():
		bits.append(backColours[back])
	else:
		bits.append("49")

	for i in range(0,len(bits)):
		if i:
			code += ";"
		code += bits[i]

	code += "m"
	return code
