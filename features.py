import numpy as np
import pandas as pd

stock_tickers = ["TSLA", "NVDA", "AMD", "SHOP", "NFLX", "META", "AAPL", "MSFT", "GOOGL", "INTC", "ORCL", "AVGO"]

def get_DR(df):
	for period in [1, 5, 10, 20]:
		df[f"DR{period}"] = df["OHLC4"].pct_change(periods=period)
	
	df["PG"] = df["Open"]-df["Close"].shift(1)

def get_OHLC(df):
	df["OHLC4"] = (df["Open"]+df["High"]+df["Low"]+df["Close"])/4

def get_MA(df):
	for period in [5, 10, 20]:
		df[f"MA{period}"] = data["OHLC4"].rolling(window=period).mean()

def get_VOL(df):
	for period in [5, 20]:
		df[f"VOL{period}"] = data["DR1"].rolling(window=period).std()

def get_Z(df):
	period = 20
	vol_mean = df["Volume"].rolling(window=period).mean()
	vol_std = df["Volume"].rolling(window=period).std()
	df["Z-Score"] = (df["Volume"]-vol_mean)/vol_std;

def get_RSI(df):
	period = 14
	
	gains = df["DR1"].clip(lower=0).to_numpy()
	
	wgains = np.zeros_like(gains)
	wgains[period] = gains[1:period+1].mean()
	for i in range(period+1, len(gains)):
		wgains[i] = (wgains[i-1]*(period-1) + gains[i]) / period
	
	losses = -df["DR1"].clip(upper=0).to_numpy()
	
	wlosses = np.zeros_like(losses)
	wlosses[period] = losses[1:period+1].mean()
	for i in range(period+1, len(losses)):
		wlosses[i] = (wlosses[i-1]*(period-1) + losses[i]) / period
	
	df["RS"] = wgains/wlosses
	df["RSI"] = 100-100/(1+df["RS"])

def get_features(df):
	get_OHLC(df)
	get_DR(df)
	get_MA(df)
	get_VOL(df)
	get_RSI(df)
	get_Z(df)

for ticker in stock_tickers:
	data = pd.read_csv(f"./data/{ticker}.csv")
	data = data.set_index("Date", drop=True)
	data = data.round(decimals=2)
	
	get_features(data)
	data.to_csv(f"./data/{ticker}.csv", index=True)