from enum import Enum
from pydantic import BaseModel, conint


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"

class UserCreate(BaseModel):
    username: str
    age: int
    gender: GenderEnum

class UserUpdate(BaseModel):
    username: str | None =None
    age: int | None =None

class UserDelete(BaseModel):
    username: str
    age: int

class UserSearch(BaseModel):
    username: str | None =None
    age: conint(gt=0) | None =None
    gender: GenderEnum | None =None