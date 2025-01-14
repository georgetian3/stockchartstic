


from sqlalchemy import select

from models.database import get_session
from models.models import OHLCV, OHLCVList


async def get_ohlcv_list(symbol: str) -> list[OHLCV]:
    async with get_session() as session:
        ohlcvs: list[OHLCV] = (await session.exec(select(OHLCV).where(OHLCV.symbol == symbol.lower()).order_by(OHLCV.timestamp))).scalars()

    return list(ohlcvs)
    l = OHLCVList()
    for ohlcv in ohlcvs:
        print(ohlcv, type(ohlcv))
        l.timestamp.append(ohlcv.timestamp)
        l.open.append(ohlcv.open)
        l.high.append(ohlcv.high)
        l.low.append(ohlcv.low)
        l.close.append(ohlcv.close)
        l.volume.append(ohlcv.volume)
    return l