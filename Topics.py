import requests
import pandas as pd
import os

# API Key
API_KEY = os.environ['API_KEY']

# The base URL for the Augmento.ai API
BASE_URL = 'https://api.augmento.ai/v0.1'

# The endpoint to get the topics
topics_endpoint = '/topics'

# The headers including the API key
headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Making the GET request to fetch the topics
response = requests.get(f'{BASE_URL}{topics_endpoint}', headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON to get the topics dictionary
    topics = response.json()
    print("Topics retrieved successfully:")
    print(topics)
else:
    print(f"Error: {response.status_code} - {response.text}")

# Assuming you have a cryptocurrency token, e.g., 'BTC' for Bitcoin
crypto_token = 'BTC'

# Prefix the topics with the crypto token
prefixed_topics = {int(k): f"{crypto_token}_{v}" for k, v in topics.items()}

# Assuming `data` is your list of data from the earlier query, we'll convert it to a DataFrame
data = [
    {'counts': [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 7, 2, 0, 0, 0, 0, 0, 7, 0, 0, 10, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 5, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 2, 3], 'datetime': '2024-07-01T00:00:00Z', 't_epoch': 1719792000},
    # Add the rest of your data here...
]

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Expanding the 'counts' list into separate columns using the prefixed topics
counts_df = pd.DataFrame(df['counts'].tolist(), columns=[prefixed_topics[i] for i in range(len(prefixed_topics))])

# Combine with the original DataFrame
df = pd.concat([df.drop('counts', axis=1), counts_df], axis=1)

# Display the DataFrame
print(df)
