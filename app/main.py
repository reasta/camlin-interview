from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from custom_types import User, Token
from security import authenticate_user, create_access_token, get_current_user
from rates import validate_wallet_input, calculate_wallet, add_to_wallet, sub_from_wallet
from constants import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

@app.post("/token", response_model=Token)
# This endpoint is taking a form data with username and password as an argument and returning a token.
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/wallet")
async def get_wallet(
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''This API is returning the wallet for value in EUR, USD and JPY converted to PLN. As well as the total value of the wallet in PLN'''
    return {"Wallet": await calculate_wallet(current_user.wallet)}

@app.post("/wallet/add/{currency}/{amount}", dependencies=[Depends(validate_wallet_input)])
async def insert_into_wallet(
    currency: str,
    amount: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''this API is adding the amount of currency into the wallet'''
    current_user = add_to_wallet({currency: amount}, current_user)
    ret = await calculate_wallet(current_user.wallet)
    return ret

@app.post("/wallet/sub/{currency}/{amount}", dependencies=[Depends(validate_wallet_input)])
async def substract_from_wallet(
    currency: str,
    amount: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''this API is substracting the amount of currency from the wallet'''
    current_user = sub_from_wallet({currency: amount}, current_user)
    ret = await calculate_wallet(current_user.wallet)
    return ret
