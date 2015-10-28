import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

#for test
import threadReq

class Crawler:	
	visited = []
	walkList = []
	regex = '^http[s]?://'
	req = requests

	def walk(self, walkList, depth):
		self.walkList = walkList
		for layer in range(depth):
			print('layer:', layer)
			
			#singo thread
			links = []
			for url in self.walkList:
				print(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S '),url)
				html = self.req.get(url,verify=False).text
				soup = BeautifulSoup(html,'lxml')
				links += self.findLink(soup)

			#eight thread
			#links = threadReq.threadWalk(self.walkList,self.req)

			self.visited += self.walkList
			self.walkList = self.urlFilter(links,self.visited,self.regex)

	def getUrlDiscover(self):
		return self.visited + self.walkList

	def setRegex(self, regex):
		self.regex = regex

	def login(self, url, username, password):
		data = {
			'username': username,
			'password': password
		}
		self.req = self.req.Session()
		self.req.post(url,data)

	@staticmethod
	def urlFilter(links, visited, regex):
		linkTmp = []
		for link in links:
			if (
					link not in visited and
					link not in linkTmp and
					re.match(regex,link)
				):
					linkTmp.append(link)
		return linkTmp

	@staticmethod
	def findLink(soup):
		links = []
		for a in soup.find_all('a'):
			if a.has_attr('href'):
				links.append(a['href'])
		return links
