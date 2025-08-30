import requests
import pandas as pd


def main(url):
    with requests.Session() as req:
        data = {
            "data": {
                "attributes": {
                    "email": "business@muneerahmad.com",  # Insert Your Email
                    "password": "pass",  # Insert Your Password
                },
                "type": "user_login",
            }
        }
        req.post(url, data=data)
        params = {
            "d": "2020-12",
            "df": "2020-03",
            "dt": "2021-03",
            "e": "1",
            "l": "1",
            "ot": "1",
        }
        r = req.get(
            "https://app.datafinder.ae/prices-and-transactions/record-data",
            params=params,
        )
        df = pd.read_html(r.content)
        print(df)


main("https://app.datafinder.ae/api/v1/user/login")
