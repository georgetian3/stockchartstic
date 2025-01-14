


import asyncio
from datetime import UTC, datetime

from datasources.yahoo import YahooDataSource


async def main():

    ds = YahooDataSource()


    def datetime_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    data = await ds.query(
        symbol='AAPL',
        interval='1m',
        # range='5d',
        start=datetime(2025, 1, 7, 12, tzinfo=UTC),
        end=datetime(2025, 1, 7, 16, tzinfo=UTC)
    )


    # await ds.save(data)


    # ts = data.chart.result[0].timestamp
    # print(len(ts))
    # pprint(ts[:10] + [ts[-1]])

    # print(json.dumps(data.model_dump(), indent=2, default=datetime_serializer))

asyncio.run(main())