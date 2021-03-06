import os
import re
import socket
import sys
import time
import threading
from queue import Queue

import retrying

import urllib.request, parser
from bs4 import BeautifulSoup
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
q = Queue(7000)
def ask(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
    req = urllib.request.Request(url=url, headers=head)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    return html

k = 0
mutex = threading.Lock()
socket.setdefaulttimeout(20)

@retrying.retry( wait_random_min = 1000,wait_random_max =5000)
def downloadpic(t):
    # time.sleep(t)
    global k
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Referer': 'https://www.pixivacg.com/'}
    try:
        if mutex.acquire():
            items = q.get()
            k += 1
            name = "D:\\爬虫图片\\"
            name = name + str(k) + '.jpg'
            mutex.release()
            print(k)
        if k >= 1000:
            sys.exit(0)
        req = urllib.request.Request(url=items, headers=head)
        res = urllib.request.urlopen(req, timeout=20)

        f = open(name, 'wb')
        f.write(res.read())
        f.close()
        if os.path.getsize(name) == 0:
            os.remove(name)
        res.close()
    except Exception as e:
        print(e)
        q.put(items)
        print(items + "  is back")
        raise e




def download():
    thread_list = []
    while not q.empty():
        thread_list.clear()
        for index in range(1, 12):
            t = threading.Thread(target=downloadpic,args=(index,))
            thread_list.append(t)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
            print(t.getName())
        for t in thread_list:
            t.join()
            print(t.getName() + "  is end")


def get_urlTwo(html):
    html = ask(html)
    soup = BeautifulSoup(html, 'html.parser')
    for item in soup.find_all('div',class_='wp-caption aligncenter'):
        item = str(item)
        list = re.findall(findload,item)
        for img_http in list:
            q.put(img_http)

def get_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    for items in soup.find_all('div',class_='post-module-thumb'):
        items = str(items)
        list = re.findall(findimg,items)
        for it in list:
            get_urlTwo(it)



def intourl(baseurl):
    if __name__ == '__main__':
        html = []
        for i in range(1, 2):
            html.append(ask(baseurl+'%d'%i))
            get_url(html[i-1])
            print(q.qsize())
            if q.qsize() >= 1000:
                break


def file_name(file_dir):
         for files in os.walk(file_dir):
             if os.path.getsize(files) == 0:
                 os.remove(files)


findload = re.compile('<a href="(.*?)"')
findimg = re.compile('"thumb-link" href="(.*?)"')
url = "https://www.pixivacg.com/ssd/page/"
intourl(url)
print(q.qsize())
download()
file_name("D:\\爬虫图片")