import crawler
import secret
import time
import re

def main():
	cr = crawler.Crawler()
	cr.login('http://moodle.ntust.edu.tw/login/index.php',secret.username,secret.password)
	cr.setRegex('http://moodle.ntust.edu.tw/(?!login/logout.php)')
	cr.walk(['http://moodle.ntust.edu.tw/'],3)
	
	for url in cr.getUrlDiscover():
		if re.match('http://moodle.ntust.edu.tw/pluginfile.php/[0-9]+/mod_resource/content/',url):
				print('source:' + url)

if __name__ == '__main__':
	start = time.time()
	main()
	stop = time.time()
	print('time',stop - start)
