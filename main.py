# http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile
from datasource.web import doScraping
from models.trader import instantRecommendation
from utils.readConfig import getAlertRules
import sys, getopt


def getArgs(argv):
    useProxy = 0
    verbose = 0

    try:
        opts, args = getopt.getopt(argv, "hp:v:", ["proxy=", "verbose="])
    except getopt.GetoptError:
        print("test.py -p <useProxy> -v <verbose>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -p <useProxy> -v <verbose>")
            sys.exit()
        elif opt in ("-p", "--proxy"):
            useProxy = arg
        elif opt in ("-v", "--verbose"):
            verbose = arg

    print('useProxy "', useProxy)
    print('verbose "', verbose)

    return useProxy, verbose


def main(argv):

    # read input params
    (useProxy, verbose) = getArgs(argv)

    # nemo data from web scraping
    mainTrades = doScraping(useProxy)

    # email config
    alertConfig = getAlertRules()

    # evaluate at real time based in the local config vs the market
    instantRecommendation(mainTrades, alertConfig)


if __name__ == "__main__":
    main(sys.argv[1:])
