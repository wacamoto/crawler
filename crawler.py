import requests,re
from bs4 import BeautifulSoup

def walk(walkList, layer, regex, visited = [], req = requests):
	links = []
	for url in walkList:
		html = req.get(url,verify=False).text
		soup = BeautifulSoup(html, 'lxml')
		for a in soup.find_all('a'):
			if a.has_attr('href') and re.match(regex,a['href']):
				links.append(a['href'])

		#all analysis write in analysis function
		analysis(soup)
	
	visited += walkList
	walkList = unique(links,visited)

	if layer > 0 and walkList:
		layer -= 1
		walk(walkList, layer, regex, visited, req)

def unique(links, visited = []):
	s = []
	for link in links:
		if link not in visited:
			if link not in s:
				if re.match('^http[s]?://',link):
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

def analysis(soup):
	links = soup.find_all('a')
	for link in links:
		if link.has_attr('href') and re.match('http://moodle.ntust.edu.tw/pluginfile.php/[0-9]+/mod_resource/content/',link['href']):
			print('source>>>' + link['href'])


def main():
	req = login('http://moodle.ntust.edu.tw/login/index.php','','')
	regex = 'http://moodle.ntust.edu.tw/(?!login/logout.php)'
	walk(['http://moodle.ntust.edu.tw/'],2,regex = regex,req = req)

if __name__ == '__main__':
	main()