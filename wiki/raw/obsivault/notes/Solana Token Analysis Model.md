---
created: 2024-06-24T02:16:35 (UTC +07:00)
tags: [crypto, investment, solana, analysis]
source: https://chatgpt.com/g/g-HMNcP6w7d-data-analyst/c/5b406f3d-a8ad-4f5b-850b-002818179749
author: 
---

# Solana Token Analysis Model

> ## Excerpt
> A conversational AI system that listens, learns, and challenges

---
To create a Python script that extracts Solana tokens launched this year, analyzes the best performing ones, and detects patterns or correlations, you'll need to follow these steps:

1.  **Data Extraction**: Get the list of Solana tokens launched this year and their performance data.
2.  **Data Analysis**: Analyze the performance data to identify the best performing tokens.
3.  **Pattern Detection**: Detect patterns or correlations in the data to understand why the best performing tokens did well.

Here's a step-by-step guide along with the Python code:

### Step 1: Data Extraction

First, you need a reliable source of Solana tokens and their performance data. For this example, we'll assume you have access to a web API or a dataset that provides this information. One possible source is CoinGecko, which provides extensive cryptocurrency data.

We'll use the `requests` library to fetch data from the API and the `pandas` library for data manipulation.

### Step 2: Data Analysis

We'll analyze the tokens' performance data to identify the top performers.

### Step 3: Pattern Detection

We'll use statistical and machine learning techniques to detect patterns or correlations in the data.

### Example Code

Below is a Python script that accomplishes the tasks outlined above:

```
<div><p><code id="code-lang-python"><span>import</span> requests
<span>import</span> pandas <span>as</span> pd
<span>from</span> datetime <span>import</span> datetime
<span>from</span> sklearn.linear_model <span>import</span> LinearRegression
<span>import</span> matplotlib.pyplot <span>as</span> plt

<span># Step 1: Data Extraction</span>
<span>def</span> <span>fetch_solana_tokens</span>():
    url = <span>"https://api.coingecko.com/api/v3/coins/markets"</span>
    params = {
        <span>"vs_currency"</span>: <span>"usd"</span>,
        <span>"category"</span>: <span>"solana-ecosystem"</span>,
        <span>"order"</span>: <span>"market_cap_desc"</span>,
        <span>"per_page"</span>: <span>250</span>,
        <span>"page"</span>: <span>1</span>,
        <span>"sparkline"</span>: <span>False</span>
    }
    response = requests.get(url, params=params)
    data = response.json()
    <span>return</span> data

<span>def</span> <span>filter_tokens_launched_this_year</span>(<span>tokens</span>):
    current_year = datetime.now().year
    this_year_tokens = []
    <span>for</span> token <span>in</span> tokens:
        launch_date = token.get(<span>"genesis_date"</span>)
        <span>if</span> launch_date <span>and</span> datetime.strptime(launch_date, <span>"%Y-%m-%d"</span>).year == current_year:
            this_year_tokens.append(token)
    <span>return</span> this_year_tokens

tokens = fetch_solana_tokens()
this_year_tokens = filter_tokens_launched_this_year(tokens)

<span># Step 2: Data Analysis</span>
<span>def</span> <span>analyze_performance</span>(<span>tokens</span>):
    df = pd.DataFrame(tokens)
    df[<span>'price_change_percentage_24h'</span>] = df[<span>'price_change_percentage_24h'</span>].fillna(<span>0</span>)
    best_performers = df.sort_values(by=<span>'price_change_percentage_24h'</span>, ascending=<span>False</span>).head(<span>10</span>)
    <span>return</span> best_performers

best_performers = analyze_performance(this_year_tokens)
<span>print</span>(<span>"Top Performing Tokens Launched This Year:"</span>)
<span>print</span>(best_performers[[<span>'id'</span>, <span>'symbol'</span>, <span>'name'</span>, <span>'current_price'</span>, <span>'price_change_percentage_24h'</span>]])

<span># Step 3: Pattern Detection</span>
<span>def</span> <span>detect_patterns</span>(<span>tokens</span>):
    df = pd.DataFrame(tokens)
    df = df[[<span>'id'</span>, <span>'symbol'</span>, <span>'current_price'</span>, <span>'market_cap'</span>, <span>'total_volume'</span>, <span>'price_change_percentage_24h'</span>]].dropna()
    
    <span># Correlation analysis</span>
    correlation_matrix = df.corr()
    <span>print</span>(<span>"Correlation Matrix:"</span>)
    <span>print</span>(correlation_matrix)
    
    <span># Linear regression for market cap vs. price change</span>
    X = df[[<span>'market_cap'</span>, <span>'total_volume'</span>]]
    y = df[<span>'price_change_percentage_24h'</span>]
    
    model = LinearRegression()
    model.fit(X, y)
    
    <span>print</span>(<span>"Linear Regression Coefficients:"</span>)
    <span>print</span>(model.coef_)
    
    <span># Plotting</span>
    plt.scatter(df[<span>'market_cap'</span>], df[<span>'price_change_percentage_24h'</span>])
    plt.xlabel(<span>'Market Cap'</span>)
    plt.ylabel(<span>'Price Change Percentage (24h)'</span>)
    plt.title(<span>'Market Cap vs. Price Change (24h)'</span>)
    plt.show()

detect_patterns(best_performers)

<span># Save the analyzed data to a CSV file for further analysis</span>
best_performers.to_csv(<span>'top_performing_solana_tokens.csv'</span>, index=<span>False</span>)
</code></p></div>
```

### Explanation:

1.  **Data Extraction**:
    
    -   The `fetch_solana_tokens` function fetches data from the CoinGecko API.
    -   The `filter_tokens_launched_this_year` function filters out tokens that were launched this year.
2.  **Data Analysis**:
    
    -   The `analyze_performance` function sorts tokens based on their 24-hour price change percentage and selects the top 10 performers.
3.  **Pattern Detection**:
    
    -   The `detect_patterns` function performs correlation analysis and linear regression to detect patterns in the data.
    -   It visualizes the relationship between market cap and price change percentage using a scatter plot.

### Running the Script

To run this script, ensure you have the necessary libraries installed:

```
<div><p><code id="code-lang-bash">pip install requests pandas scikit-learn matplotlib
</code></p></div>
```

This script will help you identify the best performing Solana tokens launched this year and detect patterns that may explain their performance.
