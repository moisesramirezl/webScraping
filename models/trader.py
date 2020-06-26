from notifications.email.sender import sendEmail
import re


def instantRecommendation(mainTrades, alertConfig):

    print("apply alert rules")
    for rule in alertConfig["rules"]:
        print("searching trade info for nemo:  " + str(rule["nemo"]))
        for trade in mainTrades:
            if trade.nemo == rule["nemo"]:
                # TODO cast string to int without replace
                lastPrice = float(re.sub(r",\d\d", "", trade.lastPrice))
                salePrice = float(rule["saleAlertPrice"])
                purchasePrice = float(rule["purchaseAlertPrice"])
                print(
                    "nemo: "
                    + trade.nemo
                    + " lastPrice: "
                    + str(lastPrice)
                    + " salePrice: "
                    + str(salePrice)
                    + " purchasePrice: "
                    + str(purchasePrice)
                    + " updated: "
                    + trade.hourLastPrice
                )

                if (lastPrice > salePrice):
                    sendEmail(trade, "Vende", alertConfig["mailto"])
                if (lastPrice < purchasePrice):
                    sendEmail(trade, "Compra", alertConfig["mailto"])
                break
