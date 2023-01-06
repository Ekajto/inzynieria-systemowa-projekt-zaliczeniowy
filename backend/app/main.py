from typing import Optional, Union

from pydantic import BaseSettings, validator
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import delete as dl
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declarative_base
from starlite import DTOFactory, HTTPException, Starlite, delete, get, post, put
from starlite.config.cors import CORSConfig
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite.status_codes import HTTP_404_NOT_FOUND


def build_database_uri(user: Union[str, None], password: Union[str, None], db: Union[str, None]) -> str:
    if user and password and db:
        return f"postgresql+asyncpg://{user}:{password}@postgres:5432/{db}"
    return "sqlite+aiosqlite:///test.sqlite"


class AppSettings(BaseSettings):
    POSTGRES_USER: Union[str, None] = None
    POSTGRES_PASSWORD: Union[str, None] = None
    POSTGRES_DB: Union[str, None] = None
    DATABASE_URI: str = "sqlite+aiosqlite:///test.sqlite"

    @validator("DATABASE_URI", pre=True)
    def uri_adjustment(cls, v, values):
        POSTGRES_USER = values.get("POSTGRES_USER")
        POSTGRES_PASSWORD = values.get("POSTGRES_PASSWORD")
        POSTGRES_DB = values.get("POSTGRES_DB")
        if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_DB:
            return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
        else:
            return v


settings = AppSettings()

Base = declarative_base()

sqlalchemy_config = SQLAlchemyConfig(connection_string=settings.DATABASE_URI, dependency_key="async_session")
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])


class ToDo(Base):  # type: ignore
    __tablename__ = "to_dos"

    id: Mapped[int] = Column(Integer, primary_key=True)  # type: ignore
    to_do: Mapped[str] = Column(String, nullable=False)  # type: ignore
    is_done: Mapped[str] = Column(Boolean, default=False)  # type: ignore
    create_date: Mapped[str] = Column(DateTime, default=func.now())  # type: ignore


CreateToDoDTO = dto_factory("CreateToDoDTO", ToDo, exclude=["id", "is_done", "create_date"])


async def on_startup() -> None:
    async with sqlalchemy_config.engine.begin() as conn:  # type: ignore
        await conn.run_sync(Base.metadata.create_all)


@post(path="/todos")
async def create_todo(
    data: CreateToDoDTO,  # type: ignore
    async_session: AsyncSession,
) -> None:
    todo: ToDo = data.to_model_instance()  # type: ignore
    async_session.add(todo)
    await async_session.commit()


@get(path="/todos")
async def get_todos(async_session: AsyncSession) -> list[Optional[ToDo]]:
    result = await async_session.execute(select(ToDo))
    todo: list[Optional[ToDo]] = [row[0] for row in result]
    return todo


@put(path="/todos/{todo_id:int}/done")
async def done_todo(todo_id: int, async_session: AsyncSession) -> None:
    result = await async_session.scalars(select(ToDo).where(ToDo.id == todo_id))
    todo: Optional[ToDo] = result.one_or_none()
    if not todo:
        raise HTTPException(detail=f"ToDo with ID {todo_id} not found", status_code=HTTP_404_NOT_FOUND)
    todo.is_done = True
    await async_session.commit()


@delete(path="/todos/{todo_id:int}")
async def delete_todo(todo_id: int, async_session: AsyncSession) -> None:
    await async_session.execute(dl(ToDo).where(ToDo.id == todo_id))
    await async_session.commit()


app = Starlite(
    route_handlers=[create_todo, get_todos, done_todo, delete_todo],
    on_startup=[on_startup],
    plugins=[sqlalchemy_plugin],
    cors_config=CORSConfig(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
)
