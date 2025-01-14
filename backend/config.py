import os
from typing import Any, TypeVar

from dotenv import load_dotenv


class _NoDefault: ...


class MissingEnvironmentVariable(Exception): ...


T = TypeVar("T")


def get_env(variable: str, default: T | _NoDefault = _NoDefault()) -> str | T:
    try:
        return os.environ[variable]
    except KeyError:
        if isinstance(default, _NoDefault):
            raise MissingEnvironmentVariable(
                f"Missing environment variable: {variable}"
            )
        return default


def int_or_none(x: Any) -> int | None:
    try:
        return int(x)
    except Exception:
        return None


load_dotenv()


DATABASE_HOST: str | None = get_env("DATABASE_HOST", None)
DATABASE_PORT: int | None = int_or_none(get_env("DATABASE_PORT", None))
DATABASE_NAME: str | None = get_env("DATABASE_NAME", None)
DATABASE_USERNAME: str | None = get_env("DATABASE_USERNAME", None)
DATABASE_PASSWORD: str | None = get_env("DATABASE_PASSWORD", None)
DATABASE_DRIVERNAME: str | None = get_env("DATABASE_DRIVERNAME", None)

REDIS_HOST: str = get_env("REDIS_HOST", "localhost")
REDIS_PORT: int = int(get_env("REDIS_PORT", 6379))

SERVER_PORT: int = int(get_env("SERVER_PORT", 8000))
SERVER_WORKERS: int = int(get_env("SERVER_WORKERS", 1))

ADMIN_EMAIL: str = get_env("ADMIN_EMAIL")
ADMIN_PASSWORD: str = get_env("ADMIN_PASSWORD")

SECRET: str = get_env("SECRET")

OAUTH_GOOGLE_CLIENT_ID: str | None = get_env("OAUTH_GOOGLE_CLIENT_ID", None)
OAUTH_GOOGLE_CLIENT_SECRET: str | None = get_env("OAUTH_GOOGLE_CLIENT_SECRET", None)

OAUTH_FACEBOOK_CLIENT_ID: str | None = get_env("OAUTH_FACEBOOK_CLIENT_ID", None)
OAUTH_FACEBOOK_CLIENT_SECRET: str | None = get_env("OAUTH_FACEBOOK_CLIENT_SECRET", None)

OAUTH_GITHUB_CLIENT_ID: str | None = get_env("OAUTH_GITHUB_CLIENT_ID", None)
OAUTH_GITHUB_CLIENT_SECRET: str | None = get_env("OAUTH_GITHUB_CLIENT_SECRET", None)

CHUNK_SIZE: int = int(get_env("CHUNK_SIZE", 1024 * 1024))

STORAGE_BACKEND: str = get_env("STORAGE_BACKEND", "local")