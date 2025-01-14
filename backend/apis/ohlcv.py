



from fastapi import APIRouter

from services.ohlcv import get_ohlcv_list
from models.models import OHLCVRead

router = APIRouter()


@router.get(
    "/{symbol}",
    response_model=list[OHLCVRead],
)
async def get_price(symbol: str):
    return await get_ohlcv_list(symbol)