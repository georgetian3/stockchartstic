import asyncio

from services.scrape import get_historical_bars, save_exchanges_and_instruments


async def main():
    await save_exchanges_and_instruments()
    await get_historical_bars("aapl")


asyncio.run(main())
