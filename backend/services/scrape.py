from datetime import UTC, datetime, timedelta
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

import time

from services.logging import get_logger
from models.database import get_session
from models.models import Exchange, Bar, Instrument
from settings import settings
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetStatus, AssetClass
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

logger = get_logger(__name__)

async def save_exchanges_and_instruments():

    trading_client = TradingClient(settings.alpaca_id, settings.alpaca_secret)
    logger.debug("Start asset query")
    assets = trading_client.get_all_assets(GetAssetsRequest(status=AssetStatus.ACTIVE, asset_class=AssetClass.US_EQUITY))
    logger.debug("Finish asset query")
    exchanges: list[Exchange] = []
    instruments: list[Instrument] = []
    for asset in assets:
        exchanges.append(Exchange(name=asset.exchange.upper()))
        instruments.append(Instrument(symbol=asset.symbol.upper(), exchange=asset.exchange.upper()))
    logger.debug("Start Insert")
    async with get_session() as session:
        logger.debug("Insert exchanges")
        await session.exec(insert(Exchange).values([exchange.model_dump() for exchange in exchanges]).on_conflict_do_nothing())
        logger.debug("Insert instruments")
        await session.exec(insert(Instrument).values([instrument.model_dump() for instrument in instruments]).on_conflict_do_nothing())
        await session.commit()
    logger.debug("Finish insert")

def query_historial_bars(symbol, start, end, timeframe=TimeFrame(1, TimeFrameUnit.Minute)):
    client = StockHistoricalDataClient(settings.alpaca_id, settings.alpaca_secret)
    return client.get_stock_bars(StockBarsRequest(
        symbol_or_symbols=symbol,
        start=start,
        end=end,
        timeframe=timeframe,
    ))

async def get_historical_bars(symbol: str):
    symbol = symbol.upper()
    async with get_session() as session:
        instrument = await session.get(Instrument, symbol)
    if instrument is None:
        logger.error(f"Symbol does not exist: {symbol}")
        return


    start_date = datetime(2025, 1, 1, tzinfo=UTC)
    stop = False
    while not stop:
        if start_date.month == 1:
            end_date = datetime(start_date.year, 6, 30, 23, 59, tzinfo=UTC)
            next_start_date = datetime(start_date.year, 7, 1, tzinfo=UTC)
        else:
            end_date = datetime(start_date.year, 12, 31, 23, 59, tzinfo=UTC)
            next_start_date = datetime(start_date.year + 1, 1, 1, tzinfo=UTC)
        if abs((end_date - datetime.now(tz=UTC)).total_seconds()) / 60 >= 15:
            end_date = datetime.now() - timedelta(days=1)
            stop = True
        logger.debug(f"Start bars query: {symbol}, {start_date} - {end_date}")
        query_start = time.time()
        bars = query_historial_bars(symbol, start_date, end_date)
        query_end = time.time()
        start_date = next_start_date
        logger.debug(f"Finish bars query: len {len(bars[symbol])}, took {round(query_end - query_start, 3)}s")


        BATCH_SIZE = 32767
        BATCH_SIZE = int(BATCH_SIZE / len(Bar.model_fields))


        logger.debug("Start bars insert")

        async with get_session() as session:
            for i in range(0, len(bars[symbol]), BATCH_SIZE):
                batch = [Bar.model_validate(bar, update={"instrument": symbol}).model_dump() for bar in bars[symbol][i : i + BATCH_SIZE]]
                await session.exec(
                    insert(Bar).values(batch).on_conflict_do_nothing()
                )
            await session.commit()
        logger.debug("Finish bars insert")


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
