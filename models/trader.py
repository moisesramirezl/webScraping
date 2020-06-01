from notifications.email.sender import sendEmail
import re


def instantRecommendation(mainTrades, alertConfig):

    print("apply alert rules")
    for rule in alertConfig["rules"]:
        print("searching trade info for nemo:  " + str(rule["nemo"]))
        for trade in mainTrades:
            if trade.nemo == rule["nemo"]:
                print(
                    "nemo: "
                    + trade.nemo
                    + " lastPrice: "
                    + trade.lastPrice
                    + " updated: "
                    + trade.hourLastPrice
                )
                # TODO cast string to int without replace
                if (
                    float(re.sub(r",\d\d", "", trade.lastPrice))
                    > rule["saleAlertPrice"]
                ):
                    sendEmail(trade, "Vende", alertConfig["mailto"])
                if (
                    float(re.sub(r",\d\d", "", trade.lastPrice))
                    < rule["purchaseAlertPrice"]
                ):
                    sendEmail(trade, "Compra", alertConfig["mailto"])
                break
