import requests
import pandas as pd
import os


# For aggregated topic counts
rolling_mean_param = 4

# API Key
API_KEY = os.environ['API_KEY']

# The base URL for the Augmento.ai API
BASE_URL = 'https://api.augmento.ai/v0.1'

# The endpoint for aggregated crypto sentiment data
endpoint = '/events/aggregated'

# The headers including the API key
headers = {
    'Api-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Example request parameters for crypto sentiment analysis
query_params = {
    "source": "twitter",  # Data source (e.g., twitter, reddit)
    "coin": "bitcoin",    # Cryptocurrency to analyze
    "bin_size": "1H",     # Aggregation time bin size (e.g., 1H for 1 hour, 24H for 1 day)
    "start_datetime": "2024-08-01T00:00:00Z",  # Start time in ISO 8601
    "end_datetime": "2024-08-11T00:00:00Z",    # End time in ISO 8601
    "start_ptr": 0,       # Index of the first time step
    "count_ptr": 1000       # Number of time steps (1 - 1000)
}

# Making the GET request to the API
response = requests.get(
    f'{BASE_URL}{endpoint}',
    headers=headers,
    params=query_params
)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
else:
    print(f"Error: {response.status_code} - {response.text}")
    data = []

# Dictionary of topics (provided by you)
topics = {'0': 'Hacks', '1': 'Pessimistic/Doubtful', '2': 'Banks', '3': 'Selling', 
          '4': 'Market_manipulation', '5': '(De-)centralisation', '6': 'Angry', '7': 'ETF', 
          '8': 'Leverage', '9': 'Bottom', '10': 'Institutional_money', '11': 'FOMO', 
          '12': 'Prediction', '13': 'Adoption', '14': 'Fearful/Concerned', '15': 'Portfolio', 
          '16': 'FUD_theme', '17': 'Whitepaper', '18': 'Announcements', 
          '19': 'Technical_analysis', '20': 'Flippening', '21': 'Community', 
          '22': 'Investing/Trading', '23': 'Euphoric/Excited', '24': 'Hodling', 
          '25': 'ICO', '26': 'Bearish', '27': 'Going_short', '28': 'Uncertain', 
          '29': 'Volume', '30': 'Risk', '31': 'Governance', '32': 'Ban', 
          '33': 'Cheap', '34': 'Short_term_trading', '35': 'Fork', '36': 'Progress', 
          '37': 'Shilling', '38': 'Bullish', '39': 'Happy', '40': 'Bubble', '41': 'Bots', 
          '42': 'Hopeful', '43': 'Bug', '44': 'Open_source', '45': 'Token_economics', 
          '46': 'Security', '47': 'Marketing', '48': 'Bad_news', '49': 'Due_diligence', 
          '50': 'Team', '51': 'Partnerships', '52': 'Pump_and_dump', '53': 'Sad', 
          '54': 'Panicking', '55': 'Listing', '56': 'Regulation/Politics', '57': 'Dip', 
          '58': 'Launch', '59': 'FOMO_theme', '60': 'Advice/Support', '61': 'Rebranding', 
          '62': 'Wallet', '63': 'Good_news', '64': 'Problems_and_issues', '65': 'Mining', 
          '66': 'Waiting', '67': 'Learning', '68': 'Scaling', '69': 'Fees', '70': 'Roadmap', 
          '71': 'Recovery', '72': 'Technology', '73': 'Mistrustful', '74': 'Marketcap', 
          '75': 'Positive', '76': 'Tax', '77': 'Long_term_investing', '78': 'Strategy', 
          '79': 'Competition', '80': 'Whales', '81': 'Correction', '82': 'Stablecoin', 
          '83': 'Buying', '84': 'Warning', '85': 'Annoyed/Frustrated', '86': 'Price', 
          '87': 'Use_case/Applications', '88': 'Rumor', '89': 'Scam/Fraud', 
          '90': 'Airdrop', '91': 'Optimistic', '92': 'Negative'}




# Assuming `BTC` as the cryptocurrency token
crypto_token = 'BTC'

# Prefix the topics with the crypto token
# prefixed_topics = {int(k): f"{crypto_token}_{v}" for k, v in topics.items()}

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Expanding the 'counts' list into separate columns using the prefixed topics
counts_df = pd.DataFrame(df['counts'].tolist(), columns=[topics[str(i)] for i in range(len(topics))])

# Combine with the original DataFrame
df = pd.concat([df.drop('counts', axis=1), counts_df], axis=1)

df.set_index('datetime', inplace=True)

positive_topics = [
    'Bullish', 'Optimistic', 'Hopeful', 'Good_news', 
    'Institutional_money', 'Euphoric/Excited', 'Buying', 
    'Airdrop', 'Long_term_investing', 'Happy', 'Hodling', 
    'Recovery', 'Positive', 'Technology', 'Adoption', 
    'Partnerships', 'Roadmap', 'Progress', 'Flippening', 
    'Prediction', 'FOMO'
]

neutral_topics = [
    'Stablecoin', 'Open_source', 'Portfolio', 'Price', 
    'Launch', 'Waiting', 'Short_term_trading', 'Security', 
    'Announcements', 'Fees', 'Leverage', 'Fork', 'Bottom', 
    'Tax', 'Advice/Support', 'Whales', 'Mining', 'ICO', 
    'Scaling', 'Investing/Trading', '(De-)centralisation', 
    'Learning', 'Token_economics', 'Regulation/Politics', 
    'Volume', 'Rebranding', 'Wallet', 'Strategy', 
    'ETF', 'Community', 'Team', 'Use_case/Applications', 
    'Governance', 'Listing', 'Technical_analysis', 
    'Competition', 'Risk', 'Due_diligence', 'Marketcap',
    'Whitepaper'
]

negative_topics = [
    'Market_manipulation', 'Mistrustful', 'Correction', 'Warning', 
    'Sad', 'Uncertain', 'Pump_and_dump', 'Shilling', 'Cheap', 
    'Bots', 'Selling', 'Panicking', 'Problems_and_issues', 
    'Fearful/Concerned', 'FOMO_theme', 'Bad_news', 'Hacks', 
    'FUD_theme', 'Scam/Fraud', 'Angry', 'Ban', 'Bug', 
    'Pessimistic/Doubtful', 'Annoyed/Frustrated', 'Marketing', 
    'Negative', 'Dip', 'Banks', 'Bearish', 'Bubble', 'Going_short', 
    'Rumor'
]

# Aggregate counts for each category
df['Positive_Sum'] = df[positive_topics].sum(axis=1)
df['Neutral_Sum'] = df[neutral_topics].sum(axis=1)
df['Negative_Sum'] = df[negative_topics].sum(axis=1)

# Calculate the total counts for each timestamp
df['Total_Sum'] = df[['Positive_Sum', 'Neutral_Sum', 'Negative_Sum']].sum(axis=1)

# Calculate the percentage for each category
df['Positive_Percentage'] = (df['Positive_Sum'] / df['Total_Sum']) * 100
df['Neutral_Percentage'] = (df['Neutral_Sum'] / df['Total_Sum']) * 100
df['Negative_Percentage'] = (df['Negative_Sum'] / df['Total_Sum']) * 100
df[['Positive_Percentage', 'Neutral_Percentage', 'Negative_Percentage']] = df[['Positive_Percentage', 'Neutral_Percentage', 'Negative_Percentage']].round(2)

df_agg = df[['Positive_Sum', 'Neutral_Sum', 'Negative_Sum', 
          'Positive_Percentage', 'Neutral_Percentage', 'Negative_Percentage']]

# Display the updated DataFrame with the new columns
print(df_agg)

df_agg.to_excel("./" + crypto_token + "_agg.xlsx")
