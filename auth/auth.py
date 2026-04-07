from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
import uvicorn

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(creds.username)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


# доступ только для авторизованных пользователей
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"message": "protected"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
