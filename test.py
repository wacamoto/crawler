from crawler import *

def ays(soup):
	regex = 'http://moodle.ntust.edu.tw/pluginfile.php/[0-9]+/mod_resource/content/'
	links = soup.find_all('a')

	for link in links:
		if link.has_attr('href') and re.match(regex,link['href']):
			print('================================================================================')
			print('source>>>' + link['href'])

def main():
	req = login('http://moodle.ntust.edu.tw/login/index.php','b10209034','ksc286stn')
	regex = 'http://moodle.ntust.edu.tw/(?!login/logout.php)'
	walk(['http://moodle.ntust.edu.tw/'], 2, regex, ays, req=req)

if __name__ == '__main__':
	main()