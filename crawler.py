import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

#for test
import threadReq

class Crawler:
    def __init__(self): 
        self.visited = []
        self.regex = '^http[s]?://'
        self.req = requests

    def walk(self, walkList, depth):
        for _ in range(depth):
            
            #singo thread
            links = []
            for url in walkList:
                print(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S '),url)
                html = self.req.get(url,verify=False).text
                soup = BeautifulSoup(html,'lxml')
                links += self.__findLink(soup)

            #eight thread
            #links = threadReq.threadWalk(walkList,self.req)

            self.visited += walkList
            walkList = self.__urlFilter(links,self.visited,self.regex)

        self.visited += walkList

    def getUrlDiscover(self):
        return self.visited

    def setRegex(self, regex):
        self.regex = regex

    def login(self, url, username, password):
        data = {
            'username': username,
            'password': password
        }
        self.req = self.req.Session()
        self.req.post(url,data)

    def __urlFilter(links, visited, regex):
        linkTmp = []
        for link in links:
            if (
                    link not in visited and
                    link not in linkTmp and
                    re.match(regex,link)
                ):
                    linkTmp.append(link)
        return linkTmp

    def __findLink(soup):
        links = []
        for a in soup.find_all('a'):
            if a.has_attr('href'):
                links.append(a['href'])
        return links