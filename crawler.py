import re
import requests
import threading
from bs4 import BeautifulSoup

def walk(walkList, layer, regex, analysis, visited=[], req=requests):
	print(layer)
	links = []
	for url in walkList:
		print(url)
		html = req.get(url,verify=False).text
		soup = BeautifulSoup(html,'lxml')
		
		#find next layer links
		for a in soup.find_all('a'):
			if a.has_attr('href'):
				links.append(a['href'])

		#all analysis write in analysis function
		analysis(soup)
	
	visited += walkList
	walkList = unique(links,visited,regex)

	if layer > 0 and walkList:
		layer -= 1
		walk(walkList, layer, regex, analysis, visited, req)

def unique(links, visited=[], regex='^http[s]?://'):
	s = []
	for link in links:
		if (
				link not in visited and
				link not in s and
				re.match(regex,link)
			):
				s.append(link)
	return s

def login(url, username, password):
	user = {
		'username':username,
		'password':password
	}
	req = requests.Session()
	req.post(url,data=user)
	return req
