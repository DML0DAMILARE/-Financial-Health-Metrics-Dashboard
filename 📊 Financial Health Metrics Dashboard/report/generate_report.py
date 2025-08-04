import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# Setup paths
metrics_dir = "data/metrics"
report_dir = "reports"
os.makedirs(report_dir, exist_ok=True)

# Load data
profit = pd.read_csv(f"{metrics_dir}/profitability_metrics.csv")
liquid = pd.read_csv(f"{metrics_dir}/liquidity_metrics.csv")
leverage = pd.read_csv(f"{metrics_dir}/leverage_metrics.csv")

# Normalize column names
for df in [profit, liquid, leverage]:
    df.columns = df.columns.str.lower().str.strip()

# === EXCEL REPORT ===
excel_path = f"{report_dir}/financial_report.xlsx"
with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
    profit.to_excel(writer, sheet_name="Profitability", index=False)
    liquid.to_excel(writer, sheet_name="Liquidity", index=False)
    leverage.to_excel(writer, sheet_name="Leverage", index=False)

print(f"✅ Excel report saved to: {excel_path}")

# === PDF REPORT ===
pdf_path = f"{report_dir}/financial_report.pdf"
with PdfPages(pdf_path) as pdf:
    def plot_table(title, df):
        fig, ax = plt.subplots(figsize=(10, 0.4 + 0.3 * len(df)))
        ax.axis("off")
        table = ax.table(cellText=df.values,
                         colLabels=df.columns,
                         loc="center",
                         cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)
        plt.title(title, fontsize=14, weight='bold')
        pdf.savefig(fig)
        plt.close()

    def plot_bar(df, column_hint, title, ylabel):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Find 'ticker' column
        ticker_col = next((col for col in df.columns if 'ticker' in col.lower()), None)
        if not ticker_col:
            raise ValueError("❌ 'ticker' column not found in DataFrame.")

        # Find column to plot
        target_col = next((col for col in df.columns if column_hint in col.lower()), None)
        if not target_col:
            print(f"⚠️ Skipping: Column with hint '{column_hint}' not found in {df.columns.tolist()}")
            return

        ax.bar(df[ticker_col], df[target_col], color="#1f77b4")
        ax.set_title(title, fontsize=14, weight='bold')
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Company")
        ax.grid(True, linestyle='--', alpha=0.5)

        for i, val in enumerate(df[target_col]):
            ax.text(i, val, f"{val:.2f}", ha='center', va='bottom', fontsize=8)

        pdf.savefig(fig)
        plt.close()

    # Add tables
    plot_table("Profitability Metrics", profit)
    plot_table("Liquidity Metrics", liquid)
    plot_table("Leverage Metrics", leverage)

    # Add bar charts
    plot_bar(profit, 'roe', "Return on Equity (ROE)", "ROE (%)")
    plot_bar(liquid, 'current_ratio', "Current Ratio", "Ratio")
    plot_bar(leverage, 'debt_to_equity', "Debt to Equity Ratio", "Ratio")

print(f"✅ PDF report saved to: {pdf_path}")
