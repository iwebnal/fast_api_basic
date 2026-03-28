from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/", tags=["root"], summary="Главная страница")
def root():
    return "Hello World"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# python3 main.py - с использованием uvicorn
# fastapi dev main.py
# uvicorn main:app -- reload