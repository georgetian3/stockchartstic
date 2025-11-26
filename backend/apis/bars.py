from datetime import datetime

from fastapi import APIRouter

import services.bars
from models.models import BarList

router = APIRouter()


@router.get(
    "/bars",
    response_model=BarList,
)
async def get_bars(
    symbol: str, start: datetime, end: datetime, timeframe: str | None = None
):
    return await services.bars.get_bar_list(symbol, start, end, timeframe)
