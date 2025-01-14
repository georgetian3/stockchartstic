
from datetime import datetime

from pydantic import BaseModel, model_validator
from sqlmodel import Column, DateTime, Field, SQLModel


class IntId(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class Instrument(SQLModel, table=True):
    symbol: str = Field(primary_key=True, max_length=5)
    currency: str
    exchange_name: str
    full_exchange_name: str
    instrument_type: str
    first_trade_date: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    long_name: str
    short_name: str

class OHLCVRead(SQLModel):
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), unique=True))
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    volume: int | None

class OHLCV(OHLCVRead, IntId, table=True):
    symbol: str = Field(foreign_key="instrument.symbol")


class OHLCVList(BaseModel):
    timestamp: list[datetime] = []
    open: list[float | None] = []
    high: list[float | None] = []
    low: list[float | None] = []
    close: list[float | None] = []
    volume: list[float | None] = []

    @model_validator(mode="after")
    def check_lists_same_length(cls, values: "OHLCVList"):
        lists = [values.timestamp, values.open, values.high, values.low, values.close, values.volume]
        lengths = {len(list) for list in lists}
        if len(lengths) > 1:
            raise ValueError("All lists must have the same length.")
        return values