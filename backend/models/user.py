from uuid import UUID

from fastapi_users import schemas
from fastapi_users_db_sqlmodel import SQLModelBaseOAuthAccount, SQLModelBaseUserDB
from sqlmodel import Relationship


class User(SQLModelBaseUserDB, table=True):
    oauth_accounts: list["OAuthAccount"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "joined"}
    )


class OAuthAccount(SQLModelBaseOAuthAccount, table=True):
    user: User | None = Relationship(back_populates="oauth_accounts")


class UserRead(schemas.BaseUser[UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
