#http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile
import requests
from bs4 import BeautifulSoup 
from getProxies import getRandomProxy
from randomHeaders import randomHeader
from readConfig import getAlertRules
from logger import Logger
import smtplib, ssl, json, re, sys, getopt

class Trade(object):
  def __init__(self, nemo, lastPrice, dateLastPrice, hourLastPrice):
    self.nemo = nemo
    self.lastPrice = lastPrice
    self.dateLastPrice = dateLastPrice
    self.hourLastPrice = hourLastPrice

mainTrades = []

def getArgs(argv):
  try:
      opts, args = getopt.getopt(argv,"hp:v:",["proxy=","verbose="])
  except getopt.GetoptError:
      print ('test.py -p <useProxy> -v <verbose>')
      sys.exit(2)
  for opt, arg in opts:
      if opt == '-h':
        print ('test.py -p <useProxy> -v <verbose>')
        sys.exit()
      elif opt in ("-p", "--proxy"):
        useProxy = arg
      elif opt in ("-v", "--verbose"):
        verbose = arg
  return useProxy, verbose

def fetchPageContent(useProxy):
  url = 'http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile'
  headers = randomHeader(Logger)
  print ("visiting: " + url)  
  print ("header: " + str(headers))
  if(useProxy == 1):
      proxy = getRandomProxy()
      print ("proxy: " + str(proxy))
      result = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, verify=True,  timeout=30)
  else:
    result = requests.get(url, headers=headers, verify=True,  timeout=30)
  return result.content

def main(argv):
  useProxy = 0
  verbose = 0
  
  (useProxy, verbose) = getArgs(argv)

  print ('useProxy "', useProxy)
  print ('verbose "', verbose)

  soup = BeautifulSoup(fetchPageContent(useProxy), 'html.parser')

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
          print("nemo: " + trade.nemo + " lastPrice: " + trade.lastPrice + " updated: " + trade.hourLastPrice)
          #TODO cast string to int without replace
          if(int(re.sub(r',\d\d', '', trade.lastPrice)) > rule['saleAlertPrice']):
            #TODO extract method here
            message = """\
              Subject: trade alert for {}

              Vende. last price: {} date: {} {} """.format(trade.nemo, trade.lastPrice, trade.dateLastPrice, trade.hourLastPrice)
            print(message)
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(sender_email, receiver_email, message)
          if(int(re.sub(r',\d\d', '', trade.lastPrice)) < rule['purchaseAlertPrice']):
            message = """\
              Subject: trade alert for {}

              Compra, last price: {} date: {} {} .""".format(trade.nemo, trade.lastPrice, trade.dateLastPrice, trade.hourLastPrice  )
            print(message)
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
              server.login(sender_email, password)
              server.sendmail(sender_email, receiver_email, message)
          break


if __name__ == "__main__":
   main(sys.argv[1:])



