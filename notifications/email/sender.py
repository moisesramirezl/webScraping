import smtplib
import ssl


class senderConfig(object):
    pass


def getConfig():
    config = senderConfig()
    config.port = 465  # For SSL
    config.smtp_server = "smtp.gmail.com"
    config.sender_email = "tradeappalert@gmail.com"
    config.password = "tradeapppass1"
    config.context = ssl.create_default_context()
    return config


def sendEmail(trade, suggestion, mailto):
    config = getConfig()

    message = """\
      Subject: trade alert for {}

      {}. last price: {} date: {} {} """.format(
        trade.nemo,
        suggestion,
        trade.lastPrice,
        trade.dateLastPrice,
        trade.hourLastPrice,
    )
    print(message)
    with smtplib.SMTP_SSL(
        config.smtp_server, config.port, context=config.context
    ) as server:
        server.login(config.sender_email, config.password)
        server.sendmail(config.sender_email, mailto, message)
