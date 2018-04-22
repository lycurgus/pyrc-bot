import re

colours = {
		'white': '00',
		'black': '01',
		'dark_blue': '02',
		'dark_green': '03',
		'light_red': '04',
		'dark_red': '05',
		'magenta': '06', 'dark_magenta': '06',
		'orange': '07', 'dark_yellow': '07',
		'yellow': '08', 'light_yellow': '08',
		'light_green': '09',
		'cyan': '10', 'dark_cyan': '10',
		'light_cyan': '11',
		'light_blue': '12',
		'light_magenta': '13',
		'gray': '14', 'dark_gray': '14', 'dark_grey': '14', 'grey': '14',
		'light_gray': '15', 'light_grey': '15'
	}

def replace(message):
	message = re.sub(r"\$\{reset\}","\x0f",message)
	message = re.sub(r"\$\{([_a-z]+)(?:\,([_a-z]+))?\s?(b|bold)?\s?(u|ul|under|line|underline)?\}",set_colours,message)
	message = re.sub(r"\$\{[a-z]+\}","",message)
	return message

def set_colours(match):
	fore = match.group(1) if match.group(1) else None
	back = match.group(2) if match.group(2) else None
	bold = True if match.group(3) else False
	undr = True if match.group(4) else False
	code = ""
	if fore in colours.keys():
		code += "\x03"+ colours[fore]
		if back in colours.keys():
			code += ","+ colours[back]
	if bold:
		code += "\x02"
	if undr:
		code += "\x1f"
	return code
