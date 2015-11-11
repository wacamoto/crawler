import crawler
import secret
import time
import re

def main():
    cr = crawler.MoodleCrawler(secret.username, secret.password)
    cr.startWalk()
    cr.getSource()

if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print('time',stop - start)
