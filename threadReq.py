import time
import datetime
import requests
import threading
from bs4 import BeautifulSoup
import queue as Queue

class Walker(threading.Thread):
	def __init__(self, links, queue, req): 
		threading.Thread.__init__(self)
		self._queue = queue
		self.links = links
		self.req = req

	def run(self):
		while True:
			link = self._queue.get()
			if isinstance(link, str) and link == 'exit':
				break
			print(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S '),link)
			try:
				html = self.req.get(link,verify=False).text
				soup = BeautifulSoup(html,'lxml')
				self.links += self.findLink(soup)
			except:
				pass

	@staticmethod
	def findLink(soup):
		links = []
		for a in soup.find_all('a'):
			if a.has_attr('href'):
				links.append(a['href'])
		return links

def bulidWalkers(links, queue, req, size):
	walkers = []
	for _ in range(size):
		walker = Walker(links, queue, req)
		walker.start() 
		walkers.append(walker)
	return walkers

def threadWalk(walkList, req):
	links = []
	queue = Queue.Queue()
	walkers = bulidWalkers(links, queue, req, 8)

	for url in walkList:
		queue.put(url)
	for worker in walkers:
		queue.put('exit')
	for worker in walkers:
		worker.join()
	
	return links
	