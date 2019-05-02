# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:15:33 2019

@author: Chi
"""
# -*- coding: utf-8 -*-
#import urllib.request, urllib.parse, urllib.error
#import ssl

import requests

from bs4 import BeautifulSoup, Comment

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import threading

#from urllib.error import URLError, HTTPError, ContentTooShortError
###################
from fake_useragent import UserAgent

ua = UserAgent()
'''
options = Options()
options.add_argument('-headless')
options.add_argument(f'user-agent={ua.random}')
'''
rest = open('rest.txt','r')
urlapi ='http://api.ip.data5u.com/dynamic/get.html?order=109854aae7cc60f4ebfd7ca4537f6959&sep=3'
'''
def get_ip():
    res = requests.get(urlapi).content.decode()
    ip = res.rstrip()
    return ip
ip = get_ip()
'''

def play_around(line):
    start = time.time()
    options = Options()
    options.add_argument('-headless')
    options.add_argument(f'user-agent={ua.random}')
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': ip,
        'ftpProxy': ip,
        'sslProxy': ip,
        })
    driver = webdriver.Firefox(proxy=proxy, executable_path='geckodriver',options=options)
    site = line.rstrip()
    driver.get(site)
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.component_entry"))) #element
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.mean_tray")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # check audio and del
    try:
        for span in soup.find_all("span", class_='unit_listen'):
            span.decompose()
    except:
        print('no audio')
    for auto in soup.find_all('autolink'):
        auto.unwrap()
    for word_dic in soup.find_all('span', class_='u_word_dic'):
        word_dic.unwrap()
    for pinyin in soup.find_all('span', class_='pinyin'):
        pinyin.decompose()
    word_word = soup.find_all("strong", class_='word') # add word
    word_simple_mean = soup.find_all('p', class_='entry_mean')
    word_mean = soup.find("div", class_='mean_tray') # add meaning
    for stuff in word_mean(text=lambda text: isinstance(text, Comment)):
        stuff.extract()

    try:
        word_tit = word_word[0].get_text()
        outputline = word_tit + '\n' + word_tit + str(word_simple_mean[0]) + str(word_mean) + '\n</>\n'
        end = time.time()
        print(str(end - start))
    except:
        outputline = 'NOT FOUND' + line + '\n</>\n'
    return outputline


c = 0
with open('rest_result.txt','w') as fout:
    fout.writelines(play_around(line) for line in rest)
    c += 1
    print(c)
fout.close()


class GetIpThread(threading.Thread):
    def __init__(self,fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond=fetchSecond
    def run(self):
        global ip
        while True:
            res = requests.get(urlapi).content.decode()
            ip = res.split('\n')
            ip = res.rstrip()
            time.sleep(self.fetchSecond)

if __name__=='__main__':
    urlapi ='http://api.ip.data5u.com/dynamic/get.html?order=109854aae7cc60f4ebfd7ca4537f6959&sep=3'
    fetchSecond = 5
    GetIpThread(fetchSecond).start()
