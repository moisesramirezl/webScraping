#http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile
import requests
from bs4 import BeautifulSoup 

class Trade(object):
    def __init__(self, nemo, lastPrice):
        self.nemo = nemo
        self.lastPrice = lastPrice

mainTrades = []

# for live scraping use
# url = 'http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile'
# print("visiting... " + url)
# headers = {
#   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
#   'AppleWebKit/537.36 (KHTML, like Gecko)'
#   'Chrome/64.0.3282.167 Safari/537.36'
# }
        
# result = requests.get(url, headers=headers,verify=True)

soup = BeautifulSoup(open("./page.html"), 'html.parser')
mainTradesNemoDiv = soup.findAll("span", {"class": "clsConstituyentes"})

itemCount = 0
for trade in mainTradesNemoDiv:
  mainTrades.append(Trade(trade.contents[0].strip(), 1))
  itemCount+=1


for trade in mainTrades:
    print(trade.nemo)