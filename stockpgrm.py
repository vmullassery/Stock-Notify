import finnhub
import websocket
import json
import math
from notify_run import Notify
# Configure API key
configuration = finnhub.Configuration(
    api_key={
        'token': '<bs91427rh5re5dkf82bg>' # Replace this
    }
)
finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

returnString = ""
stockList = []
priceList = []
lastPriceList = []
currentTime = []
lastTime = []
stockName = None
stockPrice = None
notify = Notify()

def on_message(ws, message):
	global stockList, priceList, lastPriceList, currentTime, lastTime, stockName, stockPrice, notify
	x = json.loads(message)
	y = x["data"]
	z = y[0]
	stockName = z["s"]
	stockPrice = z["p"]
	if stockName not in stockList:
		stockList.append(stockName)
		priceList.append(stockPrice)
		lastPriceList.append(stockPrice)
		lastTime.append(z["t"])
		currentTime.append(z["t"])
	else:
		pos = stockList.index(stockName)
		priceList[pos] = stockPrice
		currentTime[pos] = z["t"]
		if pChange_calc(lastPriceList[pos], priceList[pos]):
			notify.send(stockList[pos] + "has jumped 5\% in the last 5 minutes")
		if time_calc(lastTime[pos], currentTime[pos]):
			lastTime[pos] = currentTime[pos]
			lastPriceList[pos] = priceList[pos]
	print(message)

def time_calc(last, current):
	if (((math.floor(current / 1000)) - (math.floor(last / 1000)) >= 300)):
		return True
	else:
		return False

def pChange_calc(lastP, currentP):
	if (((currentP - lastP) / lastP * 100) >= 5):
		return True
	else:
		return False

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

with open('stocks.txt') as k:
	toSub = [line.rstrip('\n') for line in k]
addStrings = []
for i in toSub:
	addStrings.append("{\"type\":\"subscribe\",\"symbol\":\"" + i + "\"}")

def on_open(ws):
	global addStrings
	for k in addStrings:
		ws.send(k)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bs91427rh5re5dkf82bg",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()