


from datetime import datetime
from typing import Any
from sqlalchemy import select, and_

from models.database import get_session
from models.models import Bar, BarList


async def get_bars(symbol: str, start: datetime, end: datetime, timeframe: Any) -> list[Bar]:
    async with get_session() as session:
        bars: list[Bar] = list((
            await session.exec(
                select(Bar).where(and_(
                    Bar.instrument == symbol.upper(),
                    Bar.timestamp >= start,
                    Bar.timestamp <= end
                )
                ).order_by(Bar.timestamp)
            )
        ).scalars())

    return list(bars)



async def get_bar_list(symbol: str, start: datetime, end: datetime, timeframe: Any) -> BarList:
    bars: list[Bar] = await get_bars(symbol, start, end, timeframe)
    l = BarList()
    for bar in bars:
        l.timestamp.append(bar.timestamp)
        l.open.append(bar.open)
        l.high.append(bar.high)
        l.low.append(bar.low)
        l.close.append(bar.close)
        l.volume.append(bar.volume)
        l.trade_count.append(bar.trade_count)
        l.vwap.append(bar.vwap)
    return l