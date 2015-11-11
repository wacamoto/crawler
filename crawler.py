import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

#for test
import threadReq

class Crawler:
    def __init__(self):
        self.discover = []
        self.regex = '^http[s]?://'
        self.req = requests

    def walk(self, walkList, depth):
        for _ in range(depth):
            
            #singo thread
            links = []
            for url in walkList:
                print(self.getTime(), url)
                html = self.req.get(url, verify=False).text
                soup = BeautifulSoup(html, 'lxml')
                links += self.__findLink(soup)    

            #eight thread
            #links = threadReq.threadWalk(walkList,self.req)

            self.discover += walkList
            walkList = self.__nextURL(links, self.discover, self.regex)

        #add last discover
        self.discover += walkList

    def getdiscover(self):
        return self.discover

    def __nextURL(self, links, visited, regex):
        linkTmp = []
        for link in links:
            if (link not in visited and
                link not in linkTmp and
                re.match(regex,link)
            ):
                linkTmp.append(link)
        return linkTmp

    def __findLink(self, soup):
        links = []
        for a in soup.find_all('a'):
            if a.has_attr('href'):
                links.append(a['href'])
        return links

    @staticmethod
    def getTime():
        cur = time.time()
        t = datetime.datetime.fromtimestamp(cur)
        return t.strftime('%H:%M:%S ')


class MoodleCrawler(Crawler):
    def __init__(self, username, password):
        Crawler.__init__(self)
        Crawler.regex = 'http://moodle.ntust.edu.tw/(?!login/logout.php)'
        self.login('http://moodle.ntust.edu.tw/login/index.php', username, password)

    def getSource(self):
        reg = 'http://moodle.ntust.edu.tw/pluginfile.php/[0-9]+/mod_resource/content/'
        for url in Crawler.getdiscover(self):
            if re.match(reg, url):
                print('source:' + url)

    def login(self, url, username, password):
        data = {
            'username': username,
            'password': password
        }
        Crawler.req = requests.Session()
        Crawler.req.post(url, data)

    def startWalk(self):
        Crawler.walk(self, ['http://moodle.ntust.edu.tw/','http://moodle.ntust.edu.tw/mod/resource/view.php?id=18899'], 1)
