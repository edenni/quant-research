from time import sleep

import pandas as pd
from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

df = pd.read_csv("data/nasdaq100.csv")


class IBAPI(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.tickers = df["symbol"].values
        self.req2ticker = {}

    def nextValidId(self, orderId: int):
        for i, ticker in enumerate(self.tickers):
            contract = Contract()
            contract.symbol = ticker
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"

            self.req2ticker[orderId + i] = ticker
            print(f"Requesting data for {ticker}")
            self.reqHistoricalData(
                orderId + i,
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

            sleep(5)

    def historicalData(self, reqId, bar):
        with open(f"data/nasdaq100/{self.req2ticker[reqId]}.csv", "a") as f:
            f.write(
                f"{bar.date},{bar.open},{bar.high},{bar.low},{bar.close},{bar.volume}\n"
            )

    def historicalDataEnd(self, reqId, start, end):
        print(
            f"Ticker: <{self.req2ticker[reqId]}>\tStart: {start}, End: {end}"
        )


app = IBAPI()
app.connect("127.0.0.1", 7497, 1000)
app.run()
