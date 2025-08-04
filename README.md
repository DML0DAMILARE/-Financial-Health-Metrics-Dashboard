Financial Health Metrics Dashboard
This interactive dashboard allows users to analyze key financial health indicators — Profitability, Liquidity, and Leverage — for publicly traded companies.

Built using Python, Streamlit, and yfinance, it pulls financial data, computes core financial ratios, and presents them in a user-friendly interface with visualizations and export options.


Features    
- Visual comparison of financial metrics across companies    
- Metrics categorized into Profitability, Liquidity, and Leverage  
- CSV export for each metric category   
- Interactive company selection      
- Fully browser-based interface (no installation needed by users)


 Financial Ratios Included     
🔹 Profitability
- Return on Assets (ROA)
- Return on Equity (ROE)
- Net Profit Margin

🔹 Liquidity
- Current Ratio
- Quick Ratio

🔹 Leverage
- Debt-to-Equity Ratio
- Debt Ratio

Requirements
- Python 3.8+
- Streamlit
- yfinance
- pandas
- numpy

📌 Notes
- The data is sourced using the Yahoo Finance API via yfinance.
- Make sure you are connected to the internet when running data_collection.py.
- All processed metrics are saved as CSVs under data/metrics/.
