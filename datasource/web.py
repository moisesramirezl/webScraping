import requests

from datasource.utils.randomHeaders import randomHeader
from datasource.utils.getProxies import getFirstAliveProxy
from domain.trade import Trade
from utils.logger import Logger


from bs4 import BeautifulSoup


def fetchPageContent(useProxy):
    url = "http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile"
    headers = randomHeader(Logger)
    print("visiting: " + url)
    print("using header: " + str(headers))
    if int(useProxy):
        proxy = getFirstAliveProxy()
        print("using proxy: " + str(proxy))
        result = requests.get(
            url,
            headers=headers,
            proxies={"http": proxy, "https": proxy},
            verify=True,
            timeout=30,
        )
    else:
        result = requests.get(url, headers=headers, verify=True, timeout=30)
    return result.content


def doScraping(useProxy):

    mainTrades = []
    soup = BeautifulSoup(fetchPageContent(useProxy), "html.parser")

    mainTradesNemoDiv = soup.findAll("span", {"class": "clsConstituyentes"})
    mainTradesDiv = soup.findAll("div", {"id": "blkConstituyentes"})
    dateLastPrice = soup.find("span", {"id": "dateUltimaActu"})
    hourLastPrice = soup.find("span", {"id": "timeUltimaActu"})

    mainTradesDiv = "<html>" + str(mainTradesDiv) + "</html>"
    soupMainTradesDiv = BeautifulSoup(mainTradesDiv, "html.parser")
    mainTradesPriceDiv = soupMainTradesDiv.findAll("span", {"data-bind": "text: price"})

    itemCount = 0
    for trade in mainTradesNemoDiv:
        mainTrades.append(
            Trade(
                trade.contents[0].strip(),
                mainTradesPriceDiv[itemCount].text.strip(),
                dateLastPrice.text.strip(),
                hourLastPrice.text.strip(),
            )
        )
        itemCount += 1

    return mainTrades
