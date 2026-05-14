### Running the Script

To run this script, ensure you have the necessary libraries installed:

```bash
pip install requests pandas scikit-learn matplotlib
```

This script will help you identify the best performing Solana tokens launched this year and detect patterns that may explain their performance.

User

What type of answer can I expect 

ChatGPT

Running the script will provide you with the following insights:

1. **List of Top Performing Tokens**:
   - A table displaying the top 10 Solana tokens launched this year, sorted by their 24-hour price change percentage. This includes columns such as token ID, symbol, name, current price, and price change percentage.

   Example output:
   ```
   Top Performing Tokens Launched This Year:
           id   symbol        name  current_price  price_change_percentage_24h
   1  sol-token-1    sol1     Token1        20.45                         12.34
   2  sol-token-2    sol2     Token2         5.67                         10.21
   ...
   ```

2. **Correlation Matrix**:
   - A correlation matrix showing the correlation coefficients between different variables such as market cap, total volume, and price change percentage. This helps identify which variables are related to the tokens' performance.

   Example output:
   ```
   Correlation Matrix:
                             current_price  market_cap  total_volume  price_change_percentage_24h
   current_price                  1.000000    0.850123      0.675432                     0.234567
   market_cap                     0.850123    1.000000      0.765432                     0.345678
   total_volume                   0.675432    0.765432      1.000000                     0.456789
   price_change_percentage_24h    0.234567    0.345678      0.456789                     1.000000
   ```

3. **Linear Regression Coefficients**:
   - The coefficients of the linear regression model showing the relationship between the independent variables (market cap and total volume) and the dependent variable (price change percentage). This helps understand how changes in market cap and volume might influence the price change percentage.

   Example output:
   ```
   Linear Regression Coefficients:
   [0.002345, 0.000123]
   ```

4. **Scatter Plot**:
   - A scatter plot visualizing the relationship between market cap and price change percentage. This plot helps to visually identify any trends or patterns.

   Example plot:
   ![Scatter Plot](https://example.com/scatter_plot.png)

5. **CSV File**:
   - The analyzed data of the top-performing tokens will be saved to a CSV file (`top_performing_solana_tokens.csv`) for further analysis.