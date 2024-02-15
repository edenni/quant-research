from threading import Thread
from time import sleep

import pandas as pd
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

df = pd.read_csv("data/nasdaq100.csv")
tickers = iter(df["symbol"].values[40:].tolist())
# tickers = iter(["QQQ"])
req_ids = iter(range(1000, 2000))


class IBapi(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.req2ticker = {}

    def historicalData(self, reqId, bar):
        with open(f"data/nasdaq100/{self.req2ticker[reqId]}.csv", "a") as f:
            f.write(
                f"{bar.date},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
            )

    def historicalDataEnd(self, reqId, start, end):
        print(
            f"Ticker: <{self.req2ticker[reqId]}>\tStart: {start}, End: {end}"
        )
        get_data()


app = IBapi()
app.connect("127.0.0.1", 7497, 100)


def run_loop():
    app.run()


thread = Thread(target=run_loop, daemon=True)
thread.start()
sleep(3)


def get_data():
    ticker = next(tickers)
    req_id = next(req_ids)

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART:NASDAQ"
    contract.currency = "USD"

    app.req2ticker[req_id] = ticker
    print(f"Requesting data for {ticker} req_id: {req_id}")
    app.reqHistoricalData(
        req_id,
        contract,
        "",
        "2 Y",
        "30 mins",
        "ADJUSTED_LAST",
        1,
        1,
        False,
        [],
    )


get_data()
thread.join()
