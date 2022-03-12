import requests
from twilio.rest import Client

STOCK = "AAPL"
COMPANY_NAME = "Apple Inc"
MY_NUMBER = "+18327216070"
run_at_UTC_TIME = '14:00'  # 2 pm utc is 8 am austin

# Api keys and other
twilio_account_SID = ''***********''
twilio_Auth_tok = ''***********''
AV_STOCK_PRICE_API_KEY = ''***********''
NA_NEWS_API_KEY = '***********'

# example api endpoints
Stock_price_Daily = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
News_everything = 'https://newsapi.org/v2/everything'

# my api params
Stock_price_param = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'outputsize': 'compact',
    'datatype': 'json',
    'apikey': AV_STOCK_PRICE_API_KEY
}
News_param = {
    'apiKey': NA_NEWS_API_KEY,
    'language': 'en',
    'sortBy': 'relevance',
    'pageSize': '4',
    'qInTitle': STOCK,
    'q': COMPANY_NAME,
}




def send_message(percentage, arrow, newss_data=None):
    my_client = Client(twilio_account_SID, twilio_Auth_tok)
    message = my_client.messages \
        .create(
        body=f'{STOCK}: {arrow}{percentage}%',
        from_='+19378979427',
        to= MY_NUMBER
    )
    print(message.status)
    if newss_data == None:
        return
    for objectt in newss_data['articles']:
        title = objectt['title']
        content = objectt['content']
        date = objectt['publishedAt'][:10]
        url =  objectt['url']
        message = my_client.messages \
            .create(
                body=f'{date}\nHeadline:{title}\n\nBrief:{content}.\n{url}',
                from_='+19378979427',
                to= MY_NUMBER
            )
        print(message.status)




stock_response = requests.get(url='https://www.alphavantage.co/query', params=Stock_price_param)
data = stock_response.json()
if stock_response.status_code != 200:
    print(stock_response.status_code)

yesterday = float(list(data['Time Series (Daily)'].values())[0]['4. close'])
two_days_ago = float(list(data['Time Series (Daily)'].values())[1]['4. close'])

stock_fluc = round(yesterday - two_days_ago, 2)
if stock_fluc < 0:
    pos = '🔻'
else:
    pos = '🔺'
stock_flux_percetn = round(abs(stock_fluc / two_days_ago * 100), 1)
five_percent_margin = round(0.05 * two_days_ago, 2)
two_percent_margin = round(0.02 * two_days_ago, 2)
print(stock_flux_percetn)
if abs(stock_fluc) > two_percent_margin:
    if abs(stock_fluc) > five_percent_margin:
        print("5 percent")

        news_response = requests.get(url=News_everything, params=News_param)
        news_data = news_response.json()
        send_message( stock_flux_percetn, pos,news_data)
    else:
        print("2 percent")
        send_message(stock_flux_percetn, pos)

