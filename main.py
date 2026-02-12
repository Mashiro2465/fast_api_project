from idlelib import query
from idlelib.query import Query
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from starlette import status

from app.models.users import UserModel
from app.schemas.users import UserCreate, UserSearch
from app.schemas.users import UserUpdate
app = FastAPI()

UserModel.create_dummy()  # API 테스트를 위한 더미를 생성하는 메서드 입니다.

@app.post("/users")
async def create_user(data: UserCreate):
    user = UserModel.create(**data.model_dump())
    return user.id

@app.get("/users")
async def get_all_users():
    result = UserModel.all()
    if not result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    result = UserModel.get(id = user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result

@app.patch("/users/{user_id}")
async def update_user(data:UserUpdate, user_id: Annotated[int, Path] = Path(gt=0)):
    result = UserModel.get(id = user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    result.update(**data.model_dump())
    return result

@app.delete("/users/{user_id}")
async def delete_user(user_id: Annotated[int, Path] = Path(gt=0)):
    result = UserModel.get(id = user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    result.delete()

    return {'detail': f'User: {user_id}, Successfully Deleted.'}

@app.get("/users/search")
async def search_users(query: Annotated[UserSearch, Query()]):
    vaild_query = {key : value
                   for key, value in query.model_dump().items()
                   if value is not None}
    filtered_user = UserModel.filter(**vaild_query)
    if not filtered_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return filtered_user

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)