from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    wallet: dict

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: str

class Rates(BaseModel):
    eur: float
    usd: float
    jpy: float
    total: float | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
