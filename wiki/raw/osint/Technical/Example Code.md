### Example Code

Below is a Python script that accomplishes the tasks outlined above:

```python
import requests
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Step 1: Data Extraction
def fetch_solana_tokens():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "category": "solana-ecosystem",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def filter_tokens_launched_this_year(tokens):
    current_year = datetime.now().year
    this_year_tokens = []
    for token in tokens:
        launch_date = token.get("genesis_date")
        if launch_date and datetime.strptime(launch_date, "%Y-%m-%d").year == current_year:
            this_year_tokens.append(token)
    return this_year_tokens

tokens = fetch_solana_tokens()
this_year_tokens = filter_tokens_launched_this_year(tokens)

# Step 2: Data Analysis
def analyze_performance(tokens):
    df = pd.DataFrame(tokens)
    df['price_change_percentage_24h'] = df['price_change_percentage_24h'].fillna(0)
    best_performers = df.sort_values(by='price_change_percentage_24h', ascending=False).head(10)
    return best_performers

best_performers = analyze_performance(this_year_tokens)
print("Top Performing Tokens Launched This Year:")
print(best_performers[['id', 'symbol', 'name', 'current_price', 'price_change_percentage_24h']])

# Step 3: Pattern Detection
def detect_patterns(tokens):
    df = pd.DataFrame(tokens)
    df = df[['id', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']].dropna()
    
    # Correlation analysis
    correlation_matrix = df.corr()
    print("Correlation Matrix:")
    print(correlation_matrix)
    
    # Linear regression for market cap vs. price change
    X = df[['market_cap', 'total_volume']]
    y = df['price_change_percentage_24h']
    
    model = LinearRegression()
    model.fit(X, y)
    
    print("Linear Regression Coefficients:")
    print(model.coef_)
    
    # Plotting
    plt.scatter(df['market_cap'], df['price_change_percentage_24h'])
    plt.xlabel('Market Cap')
    plt.ylabel('Price Change Percentage (24h)')
    plt.title('Market Cap vs. Price Change (24h)')
    plt.show()

detect_patterns(best_performers)

# Save the analyzed data to a CSV file for further analysis
best_performers.to_csv('top_performing_solana_tokens.csv', index=False)
```