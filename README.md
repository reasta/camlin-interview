# Camlin 

Camlin job Interview application


## Starting application local  


Navigate to code folder, and create virtual env
```
python -m venv env
```

Next is to activate venv:
```
.\.venv\Scripts\activate
```

Install dev requirements:
```
pip install -r requirements-dev.txt  
```

Install requirements (if not dev env):
```
pip install -r requirements.txt       
```

Run server by navigating to `app/` folder and starting server:
```
cd app
uvicorn main:app --reload
```


## Starting application in docker
```
docker-compose up --build
```

## Endpoints
After running application you can access endpoint on:
```
http://127.0.0.1:8000/docs
```

### Endpoints list
| Method   | URL                                      | Description                                                                                                                         |
| -------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `POST`   | `/token`                                 | This endpoint is taking a form data with username and password as an argument and returning a token.                                |
| `GET`    | `/wallet`                                | This API is returning the wallet for value in EUR, USD and JPY converted to PLN. As well as the total value of the wallet in PLN    |
| `POST`   | `/wallet/add/{currency}/{ammount}`       | This API is adding the amount of currency into the wallet                                                                           |
| `POST`   | `/wallet/sub/{currency}/{ammount}`       | This API is substracting the amount of currency from the wallet                                                                     |



### Examples
| Endpoint                                      | Description                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/wallet/add/eur/50`      | This API call will add 50 euros to the wallet of current user                                                                                           |
| `/wallet/add/jpy/3000`    | This API call will add 3000 yens to the wallet of current user                                                                                          |
| `/wallet/sub/jpy/1500`    | This API call will remove 1500 yens from user account, if there is not enough ammount in that currency, respons will be "detail": "Not enough funds"    |
| `/wallet/sub/usd/500`     | This API call will remove 500 usd from user account, if there is not enough ammount in that currency, respons will be "detail": "Not enough funds"      |


## NBP api

Accessing api with: 
```
https://api.nbp.pl/api/exchangerates/rates/c/{cur}/?format=json
```

Providing to url needed currencies and getting response(eur, usd, jpy).  
Response is stored in DB, and using it from there in app for more efficient use of API.

note:  
For table C, NBP are updating their currencies once a day at 8:15 ( https://nbp.pl/statystyka-i-sprawozdawczosc/kursy/informacja-o-terminach-publikacji-kursow-walut/ )
