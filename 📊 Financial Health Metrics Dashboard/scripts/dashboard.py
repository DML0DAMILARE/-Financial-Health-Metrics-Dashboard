import streamlit as st
import pandas as pd
import glob
import os
import io

st.set_page_config(page_title="Financial Metrics Dashboard", layout="wide")

# Title
st.title("📊 Financial Health Metrics Dashboard")
st.markdown("Analyze **Profitability**, **Liquidity**, and **Leverage** metrics of selected companies.")

# Load metrics
def load_data(path):
    files = glob.glob(path)
    dfs = {}
    for file in files:
        key = os.path.basename(file).replace("_metrics.csv", "")
        dfs[key] = pd.read_csv(file)
    return dfs

data_dir = "data/metrics"
metrics = load_data(f"{data_dir}/*_metrics.csv")

# Check available and required metric types
required_metrics = ["profitability", "liquidity", "leverage"]
missing = [m for m in required_metrics if m not in metrics]
if missing:
    st.error(f"Missing metric files: {', '.join(missing)} in `{data_dir}`")
    st.stop()

# Company Selector
all_tickers = sorted(set(metrics['profitability']['ticker']))
selected_tickers = st.multiselect("Select companies to view", all_tickers, default=all_tickers[:3])

# Function: render chart + table + download button
def show_tab(df, title, percent_format=False):
    df_filtered = df[df['ticker'].isin(selected_tickers)].set_index("ticker")
    
    # Display chart
    st.markdown("#### 📉 Visual Comparison")
    st.bar_chart(df_filtered)

    # Display table
    st.markdown("#### 📋 Data Table")
    styled_df = df_filtered.style.format("{:.2%}" if percent_format else "{:.2f}")
    st.dataframe(styled_df)

    # Download CSV
    csv = df_filtered.reset_index().to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=f"{title.lower()}_metrics.csv",
        mime="text/csv"
    )

# Tabs
tabs = st.tabs(["📈 Profitability", "💧 Liquidity", "📉 Leverage"])

with tabs[0]:
    st.subheader("Profitability Metrics")
    st.markdown("Profitability ratios measure a company's ability to generate income relative to revenue, assets, or equity.")
    show_tab(metrics["profitability"], "Profitability", percent_format=True)

with tabs[1]:
    st.subheader("Liquidity Metrics")
    st.markdown("Liquidity ratios assess a company's ability to meet short-term obligations.")
    show_tab(metrics["liquidity"], "Liquidity")

with tabs[2]:
    st.subheader("Leverage Metrics")
    st.markdown("Leverage ratios indicate the level of financial risk and the degree of reliance on borrowed funds.")
    show_tab(metrics["leverage"], "Leverage")
