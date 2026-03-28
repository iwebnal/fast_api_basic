from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 0,
        "title": "My first book",
        "author": "Ben",
    },
    {
        "id": 1,
        "title": "My second book",
        "author": "Ann",
    }
]

@app.get("/books", tags=["root"], summary="Получить все книги")
def root():
    return books


@app.get("/books/{id}", tags=["root"], summary="Получить книгу по id")
def get_book(id: int):

    # return books[id]

    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


class NewBook(BaseModel):
    # id: int
    title: str
    author: str


@app.post("/books", tags=["root"], summary="Создать книгу")
def create_book(book: NewBook):

    # book = {
    #     "title": "My new book",
    #     "author": "John",
    # }
    # return book

    books.append({
        "id": len(books),
        "title": book.title,
        "author": book.author
    })

    for book in books:
        if book["id"] == len(books)-1:
            return book

    raise HTTPException(status_code=422, detail="Book not found")


    return book



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# python3 main.py - с использованием uvicorn
# fastapi dev main.py
# uvicorn main:app -- reload