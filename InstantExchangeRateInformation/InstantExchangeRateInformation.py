import requests
import json

api_key = "2e1b13c2585c2729fa552507"
api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"

base_currency = input("Base currency: ") 
target_currency = input("Target currency: ") 
amount = float(input(f"How much {base_currency} do you want to exchange: "))

response = requests.get(api_url + base_currency)
response_json = json.loads(response.text)

print(response_json["conversion_rates"][target_currency] * amount)
