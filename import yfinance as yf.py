import yfinance as yf
import pandas as pd


data = yf.download("ASIANPAINT.NS", period="max")


data.columns = data.columns.get_level_values(0)
data['MA5'] = data['Close'].rolling(5).mean()
data['MA20'] = data['Close'].rolling(20).mean()
data = data.dropna()
delta = data['Close'].diff()

gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
data['MA50'] = data['Close'].rolling(50).mean()
data['Daily_Return'] = data['Close'].pct_change()
data['Volatility'] = data['Close'].rolling(10).std()
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

data['RSI'] = 100 - (100 / (1 + rs))

data = data.dropna()

print(data.head())
features = data[['Close','Volume','MA5','MA20','RSI']]
target = data['Close'].shift(-1).rename("NextClose")
dataset = pd.concat([features, target], axis=1).dropna()

X = dataset[['Close','Volume','MA5','MA20','RSI']]
y = dataset['NextClose']
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X, y)
prediction = model.predict(X.iloc[[-1]])
print("Predicted next closing price:", prediction[0])
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)