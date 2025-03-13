import httpx
import pytz
from fastapi import HTTPException
from datetime import datetime
from custom_types import User
from DB import get_rates_data, get_rates_last_update, update_rates_data, update_rates
from constants import RATES_LIST

async def get_rate(cur: str) -> float:
    '''Getting latest rate for currency'''
    api_url = f"https://api.nbp.pl/api/exchangerates/rates/c/{cur}/?format=json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            rates = response.json()
            return rates['rates'][0]['ask']
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=400, detail='Error while fetching rates')

async def get_new_rates(): 
    return {rate: await get_rate(rate) for rate in RATES_LIST}

def calculate_date():
    '''Returning timestamp for today 08:15h '''
    poland_tz = pytz.timezone("Europe/Warsaw")
    now = datetime.now(poland_tz)
    today_08h = now.replace(hour=8, minute=15, second=0, microsecond=0)
    if now < today_08h:
        today_14h = today_08h.replace(day=now.day - 1)

    return int(today_08h.timestamp())

async def get_rates():
    '''NBP updates it's rate once a day at 08:15
       Storing currently walid dates to DB.
       If we have latest in db we are calculating with it, if now, we are making api call to get latest ones
    '''
    last_update = get_rates_last_update()

    if int(last_update) < calculate_date():
        new_rates = await get_new_rates()
        await update_rates(new_rates)
        return new_rates
    else: 
        return get_rates_data()

async def calculate_wallet(wallet: dict):
    '''Calculating wallet to be returned, getting valid rates, and calculate total sum'''
    rates = await get_rates()
    wallet = {k: v * float(rates[k]) for k, v in wallet.items()}
    wallet['total'] = sum(wallet.values())

    return wallet

def add_to_wallet(new_data: dict, user: User): 
    '''This function is taking a dictionary with currency and amount as an argument
    and adding this amount to the user's wallet.'''
    for k, v in new_data.items():
        user.wallet[k] += v
        new_data[k] = user.wallet[k]

    update_rates_data(new_data, user.username)

    return user

def sub_from_wallet(new_data: dict, user: User):
    '''This function is taking a dictionary with currency and amount as an argument 
    and substracting this amount from the user's wallet.'''
    for k, v in new_data.items():
        user.wallet[k] -= v
        new_data[k] = user.wallet[k]
        if(user.wallet[k] < 0):
            raise HTTPException(status_code=400, detail='Not enough funds')

    update_rates_data(new_data, user.username)

    return user

def validate_wallet_input(currency: str, amount: int):
    '''Validating wallet input to api call'''
    if amount is not int and amount < 0:
        raise HTTPException(status_code=400, detail='amount must be a positive integer')
    if currency is not str and currency not in RATES_LIST:
        raise HTTPException(status_code=400, detail='currency not supported, must be one of: eur, usd, jpy')
