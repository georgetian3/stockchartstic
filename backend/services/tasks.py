from celery import Celery

import config
from models.models import MediaVersion, VersionType

app = Celery("tasks", broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0")


@app.task
def process_new_media(media_version: MediaVersion):
    media_version = MediaVersion(type=VersionType.ORIGINAL.value)
    print('here')