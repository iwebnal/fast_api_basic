from typing import List

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI
import uvicorn

app = FastAPI()

data = {
    "email": "test@test.com",
    "bio": "Test bio",
    "age": 12,
    # "name": "John"  # для проверки с помощью ConfigDict
}


class UserSchema(BaseModel):
    email: EmailStr  # для валидации Email-а
    bio: str | None = Field(max_length=1000, description="Bio")

    model_config = ConfigDict(extra='forbid')  # extra='forbid' - запрещаем доп. параметры


class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=100)  # ge - больше либо равно 0, le - меньше либо равно


# print(UserSchema(**data))  # email='test@test.com' bio='Test bio'
# print(UserAgeSchema(**data))  # email='test@test.com' bio='Test bio' age=12 - добавился возраст

users = []


@app.post("/users", response_model=UserAgeSchema)
def create_user(user: UserAgeSchema):
    users.append(user)
    return user


@app.get("/users")
def read_users() -> List[UserAgeSchema]:  # подсказка о том какую структуру должен вернуть запрос
    return users


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
