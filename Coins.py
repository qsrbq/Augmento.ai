import requests
import os

# API Key
API_KEY = os.environ['API_KEY']

# The base URL for the Augmento.ai API
BASE_URL = 'https://api.augmento.ai/v0.1'

# The endpoint to get the list of available coins
coins_endpoint = '/coins'

# The headers including the API key
headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Making the GET request to fetch the available coins
response = requests.get(f'{BASE_URL}{coins_endpoint}', headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON to get the list of coins
    coins = response.json()
    print("List of available coins:")
    print(coins)
else:
    print(f"Error: {response.status_code} - {response.text}")
