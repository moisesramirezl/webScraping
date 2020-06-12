# http://larrainvial.finmarketslive.cl/www/index.html?mercado=chile

import logging
from datetime import datetime
from datasource.web import doScraping
from models.trader import instantRecommendation
from utils.readConfig import getAlertRules
from persistence.nemos import create
from flask import Flask

app = Flask(__name__)


def create_app():
    config_filename = 'config.py'
    app.config.from_pyfile(config_filename)

    from persistence.nemos import db
    db.init_app(app)

    return app


def saveToDatabase(mainTrades):
    for trade in mainTrades:
        data = {
            'nemo': trade.nemo,
            'lastPrice': trade.lastPrice,
            'registerDateTime': datetime.utcnow()
        }
        nemoCreated = create(data)
        print("Nemo saved in db")


@app.route('/')
def process():
    useProxy = 1

    # nemo data from web scraping
    mainTrades = doScraping(useProxy)

    # email config
    alertConfig = getAlertRules()

    # evaluate at real time based in the local config vs the market
    instantRecommendation(mainTrades, alertConfig)

    # save nemo data to historical database for analysis
    saveToDatabase(mainTrades)

    return 'Sucess'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
