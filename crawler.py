import re
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial


def walk(walkList, layer, regex, analysis, visited=[], req=requests):
	print('layer:',layer)
	links = multiWalk(walkList, analysis, req)
	visited += walkList
	walkList = unique(links,visited,regex)

	if layer > 0 and walkList:
		layer -= 1
		walk(walkList, layer, regex, analysis, visited, req)

def multiWalk(walkList, analysis, req):
	pool = ThreadPool(4)
	fun = partial(findLink, analysis, req)
	results = pool.map(fun, walkList)
	pool.close()
	pool.join()

	links = []
	for li in results:
		links += li
	return links

def findLink(analysis, req, url):
	print(url)
	links = []
	html = req.get(url,verify=False).text
	soup = BeautifulSoup(html,'lxml')
	
	#find next layer links
	for a in soup.find_all('a'):
		if a.has_attr('href'):
			links.append(a['href'])

	#all analysis write in analysis function
	analysis(soup)
	return links

def unique(links, visited=[], regex='^http[s]?://'):
	linkTmp = []
	for link in links:
		if (
				link not in visited and
				link not in linkTmp and
				re.match(regex,link)
			):
				linkTmp.append(link)
	return linkTmp

def login(url, username, password):
	user = {
		'username':username,
		'password':password
	}
	req = requests.Session()
	req.post(url,data=user)
	return req
