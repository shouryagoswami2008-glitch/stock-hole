import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="max")
    return data
def plot_stock_data(data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()  
def predict_future_price(data, days):
    data['Date'] = data.index
    data['Date'] = data['Date'].map(lambda x: x.toordinal())
    X = data['Date'].values.reshape(-1, 1)
    y = data['Close'].values
    model = LinearRegression()
    model.fit(X, y)
    future_dates = np.array([data['Date'].max() + i for i in range(1, days + 1)]).reshape(-1, 1)
    future_prices = model.predict(future_dates)
    return future_prices
ticker = input("Enter the stock ticker symbol: ")
data = get_stock_data(ticker)
plot_stock_data(data, ticker)
days = int(input("Enter the number of days to predict: "))
future_prices = predict_future_price(data, days)
print(f"Predicted future prices for the next {days} days: {future_prices}")


import requests
def get_current_stock_price(ticker):
    api_token = "7OXEAAG010CC3AZA"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            current_price = data["Global Quote"]["05. price"]
            return current_price
        else:
            return None
    else:
        return None
current_price = get_current_stock_price(ticker)
if current_price:
    print(f"The current stock price of {ticker} is: {current_price}")
else:    print("Could not retrieve the current stock price.")   
