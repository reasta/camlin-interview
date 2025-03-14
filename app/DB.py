import os
import mysql.connector
import time
from fastapi import HTTPException
from constants import RATES_LIST

DB_NAME = os.getenv('DB_NAME', '3306')
DB_UERNAME = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')

def validate_data(data, err_msg="Data not found"):
    if (data is not None):
        return data
    else:
        raise HTTPException(status_code=400, detail=err_msg)
    
def remap_user_wallet(user):
    '''remaping user wallet data, to be better used later
       mapping all currencies into dict 
    '''
    mapped_data = {'wallet':{}}
    for key, value in user.items():
        if key in RATES_LIST:
            mapped_data['wallet'].update({key:float(value)})
        else:
            mapped_data[key] = value

    return mapped_data

def get_db_connection():
    conn = mysql.connector.connect(
        host='mysql',
        user=DB_UERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

def get_user_data(username: str) -> dict:
    '''Getting user information and returning mapped data'''
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    result = validate_data(result, "User not found")

    mapped_data = remap_user_wallet(result)

    cursor.close()
    conn.close()
    return validate_data(mapped_data)

def get_rates_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM rates"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return validate_data(result)

def get_rates_last_update():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT valid FROM rates"
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return validate_data(result)['valid']


def update_rates_data(new_data, username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    for x,y in new_data.items():
        cur, val = x, y 

    query_tmp = "UPDATE users SET **CUR** = %s"
    query = query_tmp.replace("**CUR**", cur)
    cursor.execute(query, (val,))
    conn.commit()

    cursor.close()
    conn.close()
    return cursor.rowcount

async def update_rates(new_data):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    timestamp_int = int(time.time())

    query = "UPDATE rates SET eur = %s, usd = %s, jpy = %s, valid = %s"
    cursor.execute(query, (new_data['eur'], new_data['usd'], new_data['jpy'], timestamp_int))
    conn.commit()

    cursor.close()
    conn.close()
    return cursor.rowcount