import json
tradesAlertRules = {}

def getAlertRules():
  with open('tradesAlertRules.json', 'r') as inputFile:
      tradesAlertRules = inputFile.read()

  tradesAlertRulesObj = json.loads(tradesAlertRules)

  return tradesAlertRulesObj