#!/usr/bin/env python3

import socket
from lxml import etree

def get_igd_host():
	IGD_BROADCAST = "239.255.255.250"
	IGD_PORT = 1900
	#IGD_REQUEST = "M-SEARCH * HTTP/1.1\nHOST: {bc}:1900\nMAN: ssdp:discover\nMX: 10\nST: ssdp:all".format(bc=IGD_BROADCAST).encode('UTF-8')
	#IGD_REQUEST = "M-SEARCH * HTTP/1.1\r\nHOST: {bc}:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 10\r\nST: ssdp:all\r\n".format(bc=IGD_BROADCAST).encode('UTF-8')
	IGD_REQUEST = "M-SEARCH * HTTP/1.1\r\nHOST: {bc}:1900\r\nMAN: \"ssdp:discover\"\r\nMX: 10\r\nST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n".format(bc=IGD_BROADCAST).encode('UTF-8')
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.sendto(IGD_REQUEST,(IGD_BROADCAST,IGD_PORT))
	resp = s.recv(4096).decode()
	#print(resp)
	rlines = resp.split('\n')
	for rline in rlines:
		if rline.upper().startswith("LOCATION"):
			loc = rline.strip().split(":",1)[1]
	if loc:
		igd_host = loc.split(":")[1].lstrip("/")
		igd_host_port = int(loc.split(":")[2].split("/",1)[0])
		resource = loc.split(":")[2].split("/",1)[1]
	return (igd_host,igd_host_port,resource)

def get_igd_xml(host,port,resource):
	request = "GET /{} HTTP/1.1\r\nhost: {}\r\n\r\n".format(resource,host).encode("UTF-8")
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	s.send(request)
	resp = "".encode("UTF-8")
	while True:
		rcv = s.recv(2048)
		if not rcv:
			break
		resp += rcv
	s.close()
	xml = resp.decode("UTF-8").split("\r\n\r\n")[1].strip()
	#print(xml)
	return xml

def get_wan_control_url(xml):
	parser = etree.XMLParser(encoding='utf-8')
	root = etree.fromstring(xml.encode('utf-8'),parser=parser)
	namespace = root.tag.split('}')[0].lstrip('{')
	ns = '{' + namespace + '}'
	WANns = 'urn:schemas-upnp-org:service:WANIPConnection:1'
	found = [text_node for text_node in root.iter() if text_node.text == WANns]
	service = found[0].getparent()
	controlURL = service.find('{}controlURL'.format(ns)).text
	#return (controlURL,namespace)
	return (controlURL,WANns)


def buildSoapContent(ns,method,parameters):
	soapArgs = ""
	for (param, value) in parameters:
		if soapArgs != "":
			pass
			#soapArgs += "\n"
		soapArgs += "<{param}>{value}</{param}>".format(param=param,value=value)
	if len(parameters) > 0:
		pass
		#soapArgs += "\n"
	prefix = "u"
	parts = {
			'prefix': prefix,
			'arguments': soapArgs,
			'method': method,
			'target_ns': ns
			}
	soapXml = """<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding"><s:Body><{prefix}:{method} xmlns:{prefix}="{target_ns}">{arguments}</{prefix}:{method}></s:Body></s:Envelope>""".format(**parts)
	return soapXml

def buildSoapRequest(endpoint,host,port,content,method,schema):
	if not isinstance(content, bytes):
		content = content.encode("UTF-8")
	length = len(content)
	params = {
			'e': endpoint,
			'h': host,
			'p': port,
			'l': length,
			'a': "{s}#{m}".format(s=schema,m=method),
			'c': content.decode("UTF-8")
	}
	#soapRequest = "POST {e} HTTP/1.1\r\nHost: {h}:{p}\r\nContent-Type: application/soap+xml; charset=utf-8\r\nContent-Length: {l}\r\nSoapAction: {a}\r\n\r\n{c}\r\n\r\n".format(**params).encode("UTF-8")
	soapRequest = "POST {e} HTTP/1.1\r\nHost: {h}:{p}\r\nUser-Agent: Linux, UPnP/1.1, MiniUPnPc/2.0\r\nContent-Length: {l}\r\nContent-Type: text/xml\r\nSOAPAction: \"{a}\"\r\nConnection: Close\r\nCache-Control: no-cache\r\nPragma: no-cache\r\n\r\n{c}\r\n\r\n".format(**params).encode("UTF-8")
	return soapRequest

def IgdRequest(host,port,endpoint,ns,method,params):
	soapXml = buildSoapContent(ns,method,params)
	soapRequest = buildSoapRequest(endpoint,host,port,soapXml,method,ns)
	#print("sending soap request. payload is: \n\n{}".format(soapRequest.decode('UTF-8')))
	soapResponse = sendXmlRequest(host,port,soapRequest)
	#print("IGD request performed. response: \n\n{}".format(soapResponse.decode('UTF-8')))
	return soapResponse

def sendXmlRequest(host,port,payload):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	s.send(payload)
	response = "".encode("UTF-8")
	while True:
		r = s.recv(2048)
		if not r:
			break
		response += r
	s.close()
	return response

def addPortMapping(ip,port):
	params = [
		('NewRemoteHost', ""),
		('NewExternalPort', port),
		('NewProtocol', "TCP"),
		('NewInternalPort', port),
		('NewInternalClient', str(ip)),
		('NewEnabled', 1),
		('NewPortMappingDescription', "auto"),
		('NewLeaseDuration', 30)
		]
	(h,p,r) = get_igd_host()
	xml = get_igd_xml(h,p,r)
	(controlURL,ns) = get_wan_control_url(xml)
	resp = IgdRequest(h,p,controlURL,ns,"AddPortMapping",params)
	http_status = resp.decode('UTF-8').split('\n',1)[0].strip()
	return http_status.split(" ")[1] == "200"

def delPortMapping(port):
	params = [
		('NewRemoteHost', ""),
		('NewExternalPort', port),
		('NewProtocol', "TCP")
		]
	(h,p,r) = get_igd_host()
	xml = get_igd_xml(h,p,r)
	(controlURL,ns) = get_wan_control_url(xml)
	resp = IgdRequest(h,p,controlURL,ns,"DeletePortMapping",params)
	http_status = resp.decode('UTF-8').split('\n',1)[0].strip()
	return http_status.split(" ")[1] == "200"

def getExternalIpAddress():
	(h,p,r) = get_igd_host()
	xml = get_igd_xml(h,p,r)
	(controlURL,ns) = get_wan_control_url(xml)
	resp = IgdRequest(h,p,controlURL,ns,"GetExternalIPAddress",())
	http_status = resp.decode('UTF-8').upper().split('\n',1)[0].strip()
	#print(resp)
	if http_status.split(" ")[1] != "200":
		return None
	rxml = etree.fromstring(resp.decode('UTF-8').split('\r\n\r\n',1)[1].strip())
	for node in rxml.iter():
		if node.tag == "NewExternalIPAddress":
			result = node.text
	return result

if __name__ == "__main__":
	#print(getExternalIpAddress())
	print(addPortMapping("10.0.0.3",47553))
	#print(delPortMapping(4321))
