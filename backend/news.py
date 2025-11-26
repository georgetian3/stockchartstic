import logging

from settings import SETTINGS

logging.basicConfig(level=SETTINGS.log_level)

from alpaca.data.live.news import News, NewsDataStream  # noqa: E402

news_stream = NewsDataStream(SETTINGS.alpaca_id, SETTINGS.alpaca_secret)


async def news_handler(news: News | dict) -> None:
    print(news)


news_stream.subscribe_news(news_handler, "*")

news_stream.run()
