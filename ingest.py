import yfinance as yf

stock_tickers = ["TSLA", "NVDA", "AMD", "SHOP", "NFLX", "META", "AAPL", "MSFT", "GOOGL", "INTC", "ORCL", "AVGO"]
time_period = "5y"

data = yf.download(stock_tickers, period=time_period)
data.columns = data.columns.swaplevel(0, 1)
data = data.sort_index(axis=1)

for ticker in stock_tickers:
	data[ticker].to_csv(f"./data/{ticker}.csv", index=True)

print(data)