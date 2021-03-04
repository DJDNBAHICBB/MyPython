
import re
import sys
import time
import threading
from queue import Queue
import retrying

import urllib.request, parser
from bs4 import BeautifulSoup
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



mutex = threading.Lock()

@retrying.retry( wait_random_min = 2000,wait_random_max = 10000)
def download(baseurl,ti):
    global mutex
    html = ask(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(ti)
    global k
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Referer': 'https://www.pixivacg.com/'}
    for item in soup.find_all('div', attrs={'class': ['wp-caption aligncenter', 'entry-content']}):
        item = str(item)
        getimg = re.findall(findimg, item)
        for items in getimg:
            items = items[0]
            try:
                if mutex.acquire():
                    k += 1
                    mutex.release()
                if k >= 1000:
                    sys.exit(0)
                name = "D:\\爬虫图片\\"
                name = name + str(k) + '.jpg'
                req = urllib.request.Request(url=items, headers=head)
                res = urllib.request.urlopen(req, timeout=30)


                f = open(name, 'wb')
                f.write(res.read())
                f.close()
                print(k)
            except Exception as e:
                    print(e)
                    raise e



def intourl(baseurl):
    if __name__ == '__main__':
        q = Queue(200)
        html = ask(baseurl)
        thread_list = []
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='post-module-thumb'):
            item = str(item)
            first = re.findall(findload, item)
            for itemnxt in first:
                q.put(itemnxt)
            if q.full():
                break
        while not q.empty():
            thread_list.clear()
            for index in range(1,8):
                t = threading.Thread(target=download,args = (q.get(),index))
                thread_list.append(t)
            for t in thread_list:
                t.setDaemon(True)
                t.start()
                print(t.getName())
            for t in thread_list:
                t.join()
                print(t.getName()+"  is end")




findload = re.compile('<a class="thumb-link" href="(.*?)"')
findimg = re.compile('<div class="wp-caption aligncenter"><a href="(.*?)" | src="(.*?)" alt=')
url = "https://www.pixivacg.com/"
intourl(url)
