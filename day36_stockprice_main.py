import requests
import os
from twilio.rest import Client


os.environ['ALPHA_API_KEY'] = 'KEITELNHX9P212DU'
os.environ['NEWS_API_KEY'] = 'd8ae79097e6348b69f44d7692d729410'
os.environ['twilio_account_sid'] = 'AC0ec74fab0b169cb462e3ed29ab0b014f'
os.environ['twilio_auth_token'] = 'be3f3f793e2995675c8412993a11a0b4'
os.environ['my_twilio_num'] = '+18584086785'

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ALPHA_API_KEY = os.environ.get("ALPHA_API_KEY")
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
twilio_account_sid = os.environ.get('twilio_account_sid')
twilio_auth_token = os.environ.get('twilio_auth_token')
my_twilio_num = os.environ.get('my_twilio_num')

parameters = {'function': 'TIME_SERIES_DAILY',
              'symbol': STOCK_NAME,
              'apikey': ALPHA_API_KEY
              }

stock_api = requests.get(STOCK_ENDPOINT, params=parameters)
stock_api.raise_for_status()
stock_json = stock_api.json()['Time Series (Daily)']


data_close_prices = [value for (key, value) in stock_json.items()]
yesterdays_close_price = float(data_close_prices[0]['4. close'])
day_before_close_price = float(data_close_prices[1]['4. close'])
difference = abs(yesterdays_close_price-day_before_close_price)
average = (yesterdays_close_price + day_before_close_price) / 2
percentage_difference = round((difference/average) * 100)

if percentage_difference > 5:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'q': COMPANY_NAME,
        'language': 'en'
    }

    news_api = requests.get(NEWS_ENDPOINT, params=news_params)
    news_api.raise_for_status()
    news_json = news_api.json()['articles'][:3]

    for n in range(0, 3):
        if yesterdays_close_price > day_before_close_price:
            client = Client(twilio_account_sid, twilio_auth_token)
            description = news_json[n]['description']
            description = description.replace('Tesla Inc <a href="https://www.reuters.com/companies/TSLA.O" target="_blank">(TSLA.O)</a>', 'Tesla')
            message = client.messages \
                .create(
                body=f"TSLA: 🔺{percentage_difference}%\nHeadline: {news_json[n]['title']}\nBrief: {description}",
                from_= my_twilio_num,
                to ='+15405510517'
            )
            print(message.status)

        if yesterdays_close_price < day_before_close_price:
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages \
                .create(
                body=f"TSLA: 🔻{percentage_difference}%\nHeadline: {news_json[n]['title']}\nBrief: {news_json[n]['description']}",
                from_= my_twilio_num,
                to ='+15405510517'
            )
            print(message.status)

