import asyncio
from services.scrape import save_exchanges_and_instruments, get_historical_bars


async def main():
    await save_exchanges_and_instruments()
    await get_historical_bars('aapl')

asyncio.run(main())