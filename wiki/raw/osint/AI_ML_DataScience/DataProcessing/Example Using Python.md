### Example Using Python

Here’s a simplified example using ARIMA in Python:

```python
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

# Load your data
data = pd.read_csv('tourism_inflow_thailand.csv', parse_dates=['Date'], index_col='Date')
tourism_data = data['TouristInflow']

# Plot the data
plt.plot(tourism_data)
plt.title('Historical Tourism Inflow in Thailand')
plt.xlabel('Date')
plt.ylabel('Number of Tourists')
plt.show()

# Split the data into training and testing sets
train_size = int(len(tourism_data) * 0.8)
train, test = tourism_data[:train_size], tourism_data[train_size:]

# Fit ARIMA model
model = ARIMA(train, order=(5, 1, 0))
model_fit = model.fit(disp=0)

# Make predictions
predictions = model_fit.forecast(steps=len(test))[0]

# Evaluate the model
error = mean_squared_error(test, predictions)
print(f'Test MSE: {error:.2f}')

# Plot the predictions
plt.plot(test.index, test, label='Actual')
plt.plot(test.index, predictions, label='Predicted', color='red')
plt.legend()
plt.title('Tourism Inflow Forecast')
plt.xlabel('Date')
plt.ylabel('Number of Tourists')
plt.show()
```