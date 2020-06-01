import requests
from bs4 import BeautifulSoup 
import random
from lxml.html import fromstring
from itertools import cycle

def getProxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    print(proxies)
    return proxies

def getFirstAliveProxy():
    url = 'https://httpbin.org/ip'

    proxies = getProxies()
    proxyPool = cycle(proxies)

    for i in range(1,11):
        proxy = next(proxyPool)
        print("testing proxy: " + str(proxy))
        try:
            response = requests.get(url,proxies={"http": proxy, "https": proxy})
            print("is alive... ")
            return proxy
        except:
            print("Skipping. Connnection error")
    return ''
