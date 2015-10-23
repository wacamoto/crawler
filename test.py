import re
import time
import secret
import crawler

def main():
	req = crawler.login('http://moodle.ntust.edu.tw/login/index.php',secret.username,secret.password)
	regex = 'http://moodle.ntust.edu.tw/(?!login/logout.php)'
	crawler.walk(['http://moodle.ntust.edu.tw/'],2,regex,req=req)

if __name__ == '__main__':
	start = time.time()
	main()
	stop = time.time()
	print('time:',stop - start)