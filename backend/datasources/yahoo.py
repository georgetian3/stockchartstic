

from datetime import datetime

import requests
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError

from models.database import get_session
from models.models import Bar, Instrument
from services.logging import get_logger


class BaseData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
    
logger = get_logger(__name__)

class YahooTradingPeriod(BaseData):
    timezone: str
    start: datetime
    end: datetime
    gmtoffset: int

class YahooCurrentTradingPeriod(BaseData):
    pre: YahooTradingPeriod
    regular: YahooTradingPeriod
    post: YahooTradingPeriod

class YahooMeta(BaseData):
    currency: str
    symbol: str
    exchange_name: str
    full_exchange_name: str
    instrument_type: str
    first_trade_date: datetime
    regular_market_time: datetime
    has_pre_post_market_data: bool
    gmtoffset: int
    timezone: str
    exchange_timezone_name: str
    regular_market_price: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    regular_market_day_high: float
    regular_market_day_low: float
    regular_market_volume: int
    long_name: str
    short_name: str
    chart_previous_close: float
    previous_close: float
    scale: int
    price_hint: int
    current_trading_period: YahooCurrentTradingPeriod
    trading_periods: list[list[YahooTradingPeriod]]
    data_granularity: str
    range: str
    valid_ranges: list[str]

class YahooQuote(BaseData):
    high: list[float | None]
    open: list[float | None]
    close: list[float | None]
    low: list[float | None]
    volume: list[int | None]


class YahooIndicators(BaseData):
    quote: list[YahooQuote]

class YahooResult(BaseData):
    meta: YahooMeta
    timestamp: list[datetime]
    indicators: YahooIndicators

class YahooChart(BaseData):
    result: list[YahooResult]
    error: str | None

class YahooData(BaseData):
    chart: YahooChart


def round_none(x: float | None, digits: int) -> float | None:
    if not isinstance(x, float):
        return x
    return round(x, digits)

class YahooDataSource:


    async def insert(self, data: YahooData) -> None:
        new_data = data.chart.result[0]

        instrument = Instrument(**new_data.meta.model_dump())
        instrument.symbol = instrument.symbol.lower()

        TICK_SIZE = 4


        async with get_session() as session:

            try:
                session.add(instrument)
                await session.commit()
            except IntegrityError:
                await session.rollback()

            existing: list[Bar] = list((await session.exec(
                select(Bar).where(and_(
                    Bar.symbol==instrument.symbol,
                    Bar.timestamp.in_(new_data.timestamp)
                ))
            )).scalars())

            existing_map = {point.timestamp: point for point in existing}

            for i in range(len(new_data.timestamp)):
                ohlcv = Bar(
                    symbol=instrument.symbol,
                    timestamp=new_data.timestamp[i],
                    open=round_none(new_data.indicators.quote[0].open[i], TICK_SIZE),
                    high=round_none(new_data.indicators.quote[0].high[i], TICK_SIZE),
                    low=round_none(new_data.indicators.quote[0].low[i], TICK_SIZE),
                    close=round_none(new_data.indicators.quote[0].close[i], TICK_SIZE),
                    volume=new_data.indicators.quote[0].volume[i],
                )

                if ohlcv.timestamp in existing_map:
                    if ohlcv.model_dump(exclude={"id"}) != existing_map[ohlcv.timestamp].model_dump(exclude={"id"}):
                        print('Difference')
                        print('Old', existing_map[ohlcv.timestamp])
                        print('New', ohlcv)
                    continue

                session.add(ohlcv)

            await session.commit()

    async def query(self, symbol: str, interval = None, start: datetime = None, end: datetime = None, range = None) -> YahooData:

        headers = {
            'Host': 'query2.finance.yahoo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=0, i',
        }
        logger.info(f"Yahoo query: start {start.isoformat()} end {end.isoformat()} interval {interval} range {range}")
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?"
        if interval:
            url += f"&interval={interval}"
        if range:
            url += f"&range={range}"
        if start:
            url += f"&period1={round(start.timestamp())}"
        if end:
            url += f"&period2={round(end.timestamp())}"
        logger.info(f"Yahoo URL: {url}")
        resp = requests.get(url, headers=headers)
        # async with self._session.get(url) as resp:
        #     body = await resp.read()
        if resp.status_code != 200:
            logger.warning(f"Yahoo query failed {resp.status_code}: {resp.content.decode()}")
        data = YahooData.model_validate_json(resp.content)
        await self.insert(data)
        return data
   