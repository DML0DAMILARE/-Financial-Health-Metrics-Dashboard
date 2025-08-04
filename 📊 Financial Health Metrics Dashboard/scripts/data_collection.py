import yfinance as yf
import pandas as pd
import os

# Create folders
os.makedirs("data/raw_prices", exist_ok=True)
os.makedirs("data/financials", exist_ok=True)

# List of tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']

# Date range
start_date = "2020-01-01"
end_date = "2024-12-31"

for ticker in tickers:
    try:
        # Download historical stock price data
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        hist.to_csv(f"data/raw_prices/{ticker}_prices.csv")
        print(f"Saved {ticker} stock price data.")
        
        # Download financial statement data
        fin_data = {
            'ticker': ticker,
            'currentRatio': stock.info.get('currentRatio'),
            'quickRatio': stock.info.get('quickRatio'),
            'debtToEquity': stock.info.get('debtToEquity'),
            'returnOnAssets': stock.info.get('returnOnAssets'),
            'returnOnEquity': stock.info.get('returnOnEquity'),
            'grossMargins': stock.info.get('grossMargins'),
            'operatingMargins': stock.info.get('operatingMargins'),
            'netMargins': stock.info.get('netMargins'),
            'ebitdaMargins': stock.info.get('ebitdaMargins'),
        }

        pd.DataFrame([fin_data]).to_csv(f"data/financials/{ticker}_financials.csv", index=False)
        print(f"Saved {ticker} financial data.")
    
    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")
