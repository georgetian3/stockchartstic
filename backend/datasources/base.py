# from datetime import datetime

# from pydantic import BaseModel
# from pydantic import BaseModel, ConfigDict
# from pydantic.alias_generators import to_camel


# class BaseDataSource[T]:

#     def __init__(self):
#         # self._session = aiohttp.ClientSession()
#         ...

#     async def query(self, ticker: str, interval: str, start: datetime | None = None, end: datetime | None = None, range: str | None = None) -> T:
#         raise NotImplementedError()

#     def parse(self, T):
