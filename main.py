
import re
import sys
import time
import retrying
import xlwt
import urllib.request, parser
from bs4 import BeautifulSoup
import os
import multiprocessing
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True

def ask(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
    req = urllib.request.Request(url=url, headers=head)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    return html

k = 0

def process(num):
    time.sleep(num)
@retrying.retry( wait_random_min = 2000,wait_random_max = 10000)
def download(baseurl):
    global k
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Referer': 'https://www.pixivacg.com/'}
    html = ask(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_='wp-caption aligncenter'):
        item = str(item)
        getimg = re.findall(findimg, item)
        name = "D:\\爬虫图片\\"
        if not os.path.exists(name):
            os.mkdir(name)
        for items in getimg:
            try:
                if k >= 1000:
                    sys.exit(0)
                name = name + str(k) + '.jpg'
                req = urllib.request.Request(url=items, headers=head)
                res = urllib.request.urlopen(req, timeout=30)
                f = open(name, 'wb')
                f.write(res.read())
                f.close()
                k += 1
                print(k)
            except Exception as e:
                print(e)
                raise e



def intourl(baseurl):
    if __name__ == '__main__':
        html = ask(baseurl)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='post-module-thumb'):
            item = str(item)
            first = re.findall(findload, item)
            for itemnxt in first:
                download(itemnxt)




findload = re.compile('<a class="thumb-link" href="(.*?)"')
findimg = re.compile('<div class="wp-caption aligncenter"><a href="(.*?)"')
url = "https://www.pixivacg.com/"
intourl(url)
