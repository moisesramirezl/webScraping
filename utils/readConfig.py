import json
tradesAlertRules = {}

def getAlertRules():
  with open('.userConf/tradesAlertRules.json', 'r') as inputFile:
      tradesAlertRules = inputFile.read()

  tradesAlertRulesObj = json.loads(tradesAlertRules)

  return tradesAlertRulesObj