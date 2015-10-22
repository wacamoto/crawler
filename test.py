import re
import time
from crawler import *

def ays(soup):
	links = soup.find_all('a')
	for link in links:
		if link.has_attr('href') and re.match('http://moodle.ntust.edu.tw/pluginfile.php/[0-9]+/mod_resource/content/',link['href']):
			print('============================================================')
			print('source>>>',link['href'])

def main():
	#req = login('http://moodle.ntust.edu.tw/login/index.php','','')
	regex = 'http://moodle.ntust.edu.tw/(?!login/logout.php)'
	walk(['http://moodle.ntust.edu.tw/'],2,regex,ays)

if __name__ == '__main__':
	start = time.time()
	main()
	stop = time.time()
	print('time:',stop - start)