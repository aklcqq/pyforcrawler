# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:15:33 2019

@author: Chi
"""

# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import urllib3
import requests

import time
import threading

from urllib.error import URLError, HTTPError, ContentTooShortError
###################


from fake_useragent import UserAgent

ua = UserAgent()

## ignore ssl certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://zh.dict.naver.com/api3/zhko/search?query='
urlapi ='http://api.ip.data5u.com/dynamic/get.html?order=109854aae7cc60f4ebfd7ca4537f6959&sep=3'
'''
def get_ip():
    threading.Timer(5.0, get_ip).start()
    res = requests.get(urlapi).content.decode()
    ip = res.rstrip()
    return ip

get_ip()
'''
def get_site(vocab, num_retries=4):
    check_vocab = '<strong>' + vocab + '</strong>'
    vocab = urllib.parse.quote(vocab, safe='/',encoding='utf-8')

    url = 'https://zh.dict.naver.com/api3/zhko/search?query='
    headers = {'User-Agent':ua.random}
    proxies = {'http':f'http://{ip}', "https" :f'https://{ip}'}
    print(proxies)
    
    try:
        '''
        uhp = urllib.request.ProxyHandler(proxies=proxies).Request(url + vocab, headers=headers)
        uh = urllib.request.ProxyHandler(proxies=proxies).urlopen(uhp, context=ctx)
        data = uh.read().decode()
        '''
        request = urllib.request.Request(url+vocab)
        request.add_header('User-Agent', ua.random)
        proxy_support = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        resp = urllib.request.urlopen(request)
        data = resp.read().decode()
        data = data.rstrip()
        datajs = json.loads(data)
        items = datajs['searchResultMap']['searchResultListMap']['WORD']['items']
        site_list = [item['destinationLinkKo'] for item in items if item['expEntry'] == check_vocab]
    #return site_list

    except (URLError, HTTPError, ContentTooShortError) as e:
        print('error:', e.reason)
        site_list = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return get_site(vocab, num_retries - 1)

    return site_list




fh = open('xiaocidian.txt','r')
start = time.time()

class CrawlThread(threading.Thread):
    def __init__(self,ip):
        super(CrawlThread, self).__init__()
        self.ip=ip
    def run(self):
        start = time.time()
        with open('rawre1.txt','a') as sa:
            c = 0
            for line in fh:
                vocab = line.rstrip()        
                try:
                    site_list = get_site(vocab)
                    print(site_list)
                    print(ip)
                    c += 1
                    print(c)
                    for site in site_list:
                        sa.write(site + '\n')
                except:
                    print('no',line)
                    sa.write('00000' + line + '\n')
                time.sleep(5)
            sa.close()
            stop = time.time()
        print(int(stop) - int(start))

        
class GetIpThread(threading.Thread):
    def __init__(self,fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond=fetchSecond
    def run(self):
        global ip;
        while True:
            res = requests.get(urlapi).content.decode()
            ip = res.split('\n')
            ip = res.rstrip()
            CrawlThread(ip).start()
            time.sleep(self.fetchSecond)
            
if __name__=='__main__':
    fetchSecond = 5
    GetIpThread(fetchSecond).start()



