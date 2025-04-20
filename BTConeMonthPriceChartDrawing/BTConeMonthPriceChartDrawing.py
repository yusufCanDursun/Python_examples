import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

parameters = {
    "vs_currency": "usd",
    "days": "30",  
    "interval": "daily"
    }

response = requests.get(url, params = parameters)
data = response.json()

price_data=[]

for day in data["prices"] : 
    timestamp = day[0]
    price = day[1]
    readable_date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

    price_data.append((readable_date,price))

price_array = np.array(price_data, dtype=[('date', 'U19'), ('price', 'f8')])

dates = price_array['date']
prices = price_array['price']


plt.figure(figsize=(10, 6))  
plt.plot(dates, prices, marker='o', color='b', label='Bitcoin Price')
plt.xticks(rotation=45, ha="right")  
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('Bitcoin Price for the Last 30 Days')
plt.tight_layout()  
plt.grid(True)
plt.legend()
plt.show()
