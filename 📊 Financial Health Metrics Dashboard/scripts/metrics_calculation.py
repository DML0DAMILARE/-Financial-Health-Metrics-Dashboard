import pandas as pd
import os
import glob

# Load all financials
financial_files = glob.glob("data/financials/*.csv")
metrics_df = pd.DataFrame()

for file in financial_files:
    try:
        df = pd.read_csv(file)
        metrics_df = pd.concat([metrics_df, df], ignore_index=True)
    except Exception as e:
        print(f"Failed to process {file}: {e}")

# Clean and convert columns to numeric
cols = ['currentRatio', 'quickRatio', 'debtToEquity', 'returnOnAssets', 
        'returnOnEquity', 'grossMargins', 'operatingMargins', 
        'netMargins', 'ebitdaMargins']

metrics_df[cols] = metrics_df[cols].apply(pd.to_numeric, errors='coerce')

# Compute categorized metrics
profitability = metrics_df[['ticker', 'returnOnAssets', 'returnOnEquity', 'grossMargins', 'netMargins', 'ebitdaMargins']]
liquidity = metrics_df[['ticker', 'currentRatio', 'quickRatio']]
leverage = metrics_df[['ticker', 'debtToEquity']]

# Save categorized metrics
os.makedirs("data/metrics", exist_ok=True)
profitability.to_csv("data/metrics/profitability_metrics.csv", index=False)
liquidity.to_csv("data/metrics/liquidity_metrics.csv", index=False)
leverage.to_csv("data/metrics/leverage_metrics.csv", index=False)

print("Metrics calculation complete and saved.")
