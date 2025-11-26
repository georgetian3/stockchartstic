from datetime import datetime

from pydantic import BaseModel, model_validator
from sqlmodel import Column, DateTime, Field, SQLModel


class IntId(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class Instrument(SQLModel, table=True):
    symbol: str = Field(primary_key=True)
    exchange: str = Field(foreign_key="exchange.name")


class Exchange(SQLModel, table=True):
    name: str = Field(primary_key=True)


class BarsRead(SQLModel):
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), primary_key=True)
    )
    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int | None = None
    vwap: float | None = None


class Bar(BarsRead, table=True):
    instrument: str = Field(foreign_key="instrument.symbol", primary_key=True)


class BarList(BaseModel):
    timestamp: list[datetime] = []
    open: list[float | None] = []
    high: list[float | None] = []
    low: list[float | None] = []
    close: list[float | None] = []
    volume: list[int | None] = []
    trade_count: list[int | None] = []
    vwap: list[float | None] = []

    @model_validator(mode="after")
    def check_lists_same_length(cls, values: "BarList"):
        lists = [
            values.timestamp,
            values.open,
            values.high,
            values.low,
            values.close,
            values.volume,
        ]
        lengths = {len(list) for list in lists}
        if len(lengths) > 1:
            raise ValueError("All lists must have the same length.")
        return values
