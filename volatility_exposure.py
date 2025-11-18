import yfinance as yf
import pandas as pd


# Prices
ticker = "SPY"
start_date = "2015-01-01"
prices = yf.download(ticker, start=start_date, auto_adjust=True)["Close"].dropna()
print("PRICES HEAD:")
print(prices.head())

# Returns
returns = prices.pct_change().dropna()
print("\nRETURNS HEAD:")
print (returns.head())

# Rolling Volatility
window = 60
rolling_daily_vol = returns.rolling(window).std()
rolling_annualized_vol = rolling_daily_vol * (252 ** 0.5)
print("\nROLLING ANNUALIZED VOL HEAD:")
print(rolling_annualized_vol.head(80))

target_vol = 0.2 # annualized target volatility of 15%

# Exposure Calculation
exposure = target_vol / rolling_annualized_vol 
cap = 3.0 # maximum exposure cap
exposure = exposure.clip(upper=cap)
print("\nEXPOSURE HEAD:")
print(exposure.head(80))

# Calculate Scaled Returns
scaled_returns = exposure.shift(1)*returns # shift by 1 to avoid look-ahead bias 
# I dont know the exposure for the current day when calculating today's return 
# so we use yesterday's. exposure to scale today's return.
# Its like a backtest and i calculate my returns if i had invested according to yesterday's exposure.
print("\nSCALED RETURNS HEAD:")
print(scaled_returns.head(80))

# Cumulative Returns
scaled_returns_new = scaled_returns.fillna(0) # fill NaN values with 0 for cumulative return calculation
strategy_portfolio = (1 + scaled_returns_new).cumprod()
benchmark_portfolio = (1+returns).cumprod()
strategy_profit = strategy_portfolio - 1
benchmark_profit = benchmark_portfolio - 1
print("\nSTRATEGY PORTFOLIO TAIL:")
print(strategy_portfolio.tail(10))
print("\nBENCHMARK PORTFOLIO TAIL:")
print(benchmark_portfolio.tail(10))
print("\n Final Strategy Portfolio Value:", strategy_portfolio.iloc[-1])
print(" Final Benchmark Portfolio Value :", benchmark_portfolio.iloc[-1])
print("\n Strategy total return (%) :", (strategy_portfolio.iloc[-1]-1)*100)
print("\n Benchmark total return (%)  :", (benchmark_portfolio.iloc[-1]-1)*100)






