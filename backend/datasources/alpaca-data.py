# from datetime import UTC, datetime
# from alpaca.data.historical import StockHistoricalDataClient
# from alpaca.data.requests import StockBarsRequest
# from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

# KEY = "PKAA6O7FXLMP6UXG1AJA"
# SECRET = "Drf4Tnf5bQla5qQxM0rb8BjFtzXqAgvqrDZQuV6m"

# client = StockHistoricalDataClient(KEY, SECRET, raw_data=True)

# bars = client.get_stock_bars(StockBarsRequest(
#     symbol_or_symbols="AAPL",
#     start=datetime(2020, 1, 1, 0, 0, 0, tzinfo=UTC),
#     end=datetime(2020, 1, 1, 0, 10, 0, tzinfo=UTC),
#     timeframe=TimeFrame(1, TimeFrameUnit.Minute),
# ))
# print(bars)

import requests

url = "https://paper-api.alpaca.markets/v2/assets?status=active&asset_class=us_equity&attributes="

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKAA6O7FXLMP6UXG1AJA",
    "APCA-API-SECRET-KEY": "Drf4Tnf5bQla5qQxM0rb8BjFtzXqAgvqrDZQuV6m",
}

response = requests.get(url, headers=headers)

with open("test.json", "w", encoding="utf-8") as f:
    f.write(response.text)


# # import requests

# # url = "https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=1M&start=2024-01-03T00%3A00%3A00Z&end=2024-01-08T00%3A00%3A00Z&limit=10000&adjustment=raw&feed=sip&sort=asc"

# # headers = {
# #     "accept": "application/json",
# #     "APCA-API-KEY-ID": "PKAA6O7FXLMP6UXG1AJA",
# #     "APCA-API-SECRET-KEY": "Drf4Tnf5bQla5qQxM0rb8BjFtzXqAgvqrDZQuV6m"
# # }

# # response = requests.get(url, headers=headers)

# # print(response.text)


# # from datetime import datetime
# # from pydantic import BaseModel, Field
# # import requests

# # class AlpacaStockHistoricalBarsOHLCV(BaseModel):
# #     timestamp: datetime = Field(alias="t")
# #     open: float = Field(alias="o")
# #     high: float = Field(alias="h")
# #     low: float = Field(alias="l")
# #     close: float = Field(alias="c")
# #     volume: int = Field(alias="v")
# #     trades: int = Field(alias="n")
# #     volume_weighted_average_price: float = Field(alias="vw")

# # class AlpacaStockHistoricalBars(BaseModel):
# #     bars: dict[str, list[AlpacaStockHistoricalBarsOHLCV]]
# #     next_page_token: str | None


# # def query_alpaca(symbol: str, timeframe: str, start: datetime, end: datetime, limit)

# # url = "https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=1Min&start=2024-01-03T00%3A00%3A00Z&end=2024-01-08T00%3A00%3A00Z&limit=10000&adjustment=raw&feed=sip&sort=asc"

# # headers = {
# #     "accept": "application/json",
# #     "APCA-API-KEY-ID": "PKAA6O7FXLMP6UXG1AJA",
# #     "APCA-API-SECRET-KEY": "Drf4Tnf5bQla5qQxM0rb8BjFtzXqAgvqrDZQuV6m"
# # }

# # response = requests.get(url, headers=headers)

# # print(response.text)
