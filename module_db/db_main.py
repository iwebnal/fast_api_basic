# pip install aiosqlite sqlalchemy
from typing import Annotated

import uvicorn
from dns.e164 import query
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import select

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setupdb")
async def setup_db():
    async with engine.begin() as conn:  # тут мы открываем соединение с нашей базой данных
        await conn.run_sync(Base.metadata.drop_all)  # пишем команду "run_sync" для синхронного запуска
        # drop_all - для полной очистки базы данных
        await conn.run_sync(Base.metadata.create_all)  # пишем команду "run_sync" для синхронного запуска
        # create_all - создать все таблицы со столбцами
        # Base.metadata - хранится вся информация о таблицах
    return {"message": "Database setup successful"}


# class BookCreateSchema(BaseModel):
#     title: str
#     author: str
#
# class BookSchema(BookCreateSchema):
#     id: int


class BookSchema(BaseModel):
    title: str
    author: str


@app.get("/books")
async def get_books(session: SessionDep):
    request = select(BookModel)
    result = await session.execute(request)
    books = result.scalars().all()
    return books


@app.post("/books")
async def create_book(data: BookSchema,
                      session: SessionDep):  # session: SessionDep - для работы с сессией. Получили доступ к БД
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()  # коммитим изменения в базу данных
    return {"message": "Book created successfully"}


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
