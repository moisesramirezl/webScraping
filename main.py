#http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile
import requests
from bs4 import BeautifulSoup 
from getProxies import getRandomProxy
from randomHeaders import randomHeader
from readConfig import getAlertRules
from logger import Logger
import smtplib, ssl
import json


class Trade(object):
    def __init__(self, nemo, lastPrice, dateLastPrice, hourLastPrice):
        self.nemo = nemo
        self.lastPrice = lastPrice
        self.dateLastPrice = dateLastPrice
        self.hourLastPrice = hourLastPrice

mainTrades = []


# for live scraping use
url = 'http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile'
      

headers = randomHeader(Logger)
proxy = getRandomProxy()

print ("visiting: " + url)  
print ("header: " + str(headers))
print ("proxy: " + str(proxy))

result = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, verify=True,  timeout=20)
soup = BeautifulSoup(result.content, 'html.parser')

mainTradesNemoDiv = soup.findAll("span", {"class": "clsConstituyentes"})
mainTradesDiv = soup.findAll("div", {"id":"blkConstituyentes"})
dateLastPrice = soup.find("span", {"id": "dateUltimaActu"})
hourLastPrice = soup.find("span", {"id": "timeUltimaActu"})

mainTradesDiv = "<html>" + str(mainTradesDiv) + "</html>"
soupMainTradesDiv = BeautifulSoup(mainTradesDiv, 'html.parser')
mainTradesPriceDiv = soupMainTradesDiv.findAll("span", {"data-bind":"text: price"})
 
itemCount = 0
for trade in mainTradesNemoDiv:
  mainTrades.append(Trade(trade.contents[0].strip(), 
    mainTradesPriceDiv[itemCount].text.strip(), 
    dateLastPrice.text.strip(), 
    hourLastPrice.text.strip()))
  itemCount+=1


#email config

alertConfig = getAlertRules()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "tradeappalert@gmail.com"
receiver_email = alertConfig['mailto']
password = "tradeapppass1"


context = ssl.create_default_context()


print("apply alert rules")
for rule in alertConfig['rules']:
  print("searching trade info for nemo:  " + str(rule['nemo']))
  for trade in mainTrades:
    if trade.nemo == rule['nemo']:
        print("lastPrice " + trade.lastPrice)
        #TODO cast string to int without replace
        if(int(trade.lastPrice.replace(',00','')) > rule['saleAlertPrice']):
          #TODO extract method here
          message = """\
            Subject: trade alert for {}

            Vende. last price: {} date: {} {} """.format(trade.nemo, trade.lastPrice, trade.dateLastPrice, trade.hourLastPrice)
          print(message)
          with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
             server.login(sender_email, password)
             server.sendmail(sender_email, receiver_email, message)
        if(int(trade.lastPrice.replace(',00','')) < rule['purchaseAlertPrice']):
          message = """\
            Subject: trade alert for {}

            Compra, last price: {} date: {} {} .""".format(trade.nemo, trade.lastPrice, trade.dateLastPrice, trade.hourLastPrice  )
          print(message)
          with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        break
  

# for trade in mainTrades:
#   if(trade.nemo == "LTM"):
#     if(trade.lastPrice < '900'):
#       with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
#     else:
#       print ("Aun no, precio = " + str(trade.lastPrice))