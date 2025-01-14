from enum import Enum

from fastapi import UploadFile


class CrudResult(Enum):
    OK = 0
    DOES_NOT_EXIST = 1
    NOT_AUTHORITZED = 2


async def upload_files(files: list[UploadFile]): ...
