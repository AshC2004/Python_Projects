import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="NSE Portfolio Risk Analyzer", layout="wide", page_icon="💹")

# Portfolio sample data
portfolio = pd.DataFrame([
    {"Symbol": "TCS", "Quantity": 100, "Avg Price": 3574.25, "Sector": "IT Services"},
    {"Symbol": "RELIANCE", "Quantity": 50, "Avg Price": 2456.80, "Sector": "Oil & Gas"},
    {"Symbol": "INFY", "Quantity": 150, "Avg Price": 1432.50, "Sector": "IT Services"},
    {"Symbol": "WIPRO", "Quantity": 200, "Avg Price": 445.30, "Sector": "IT Services"},
    {"Symbol": "HDFC", "Quantity": 75, "Avg Price": 2678.90, "Sector": "Banking"},
])

current_prices = {
    "TCS": 3600.50,
    "RELIANCE": 2480.10,
    "INFY": 1448.30,
    "WIPRO": 438.50,
    "HDFC": 2701.85
}

portfolio["Current Price"] = portfolio["Symbol"].map(current_prices)
portfolio["Market Value"] = portfolio["Quantity"] * portfolio["Current Price"]
portfolio["PnL"] = (portfolio["Current Price"] - portfolio["Avg Price"]) * portfolio["Quantity"]
portfolio["Weight (%)"] = portfolio["Market Value"] / portfolio["Market Value"].sum() * 100

st.title("NSE Portfolio Risk Analyzer Dashboard")
st.dataframe(portfolio.style.applymap(lambda v: "color: red" if v < 0 else "color: green", subset=["PnL"]), use_container_width=True)

st.metric("Total Portfolio Value", f"₹{portfolio['Market Value'].sum():,.2f}")
st.metric("Total P&L", f"₹{portfolio['PnL'].sum():,.2f}", delta=f"{portfolio['PnL'].sum()/portfolio['Market Value'].sum()*100:.2f}%")

st.header("Pareto Analysis: Risk Contribution by Symbol")
risk_contributions = np.random.dirichlet(np.ones(len(portfolio)),size=1)[0]
pareto_df = pd.DataFrame({"Symbol": portfolio["Symbol"], "Risk Contribution %": risk_contributions*100})
pareto_df = pareto_df.sort_values("Risk Contribution %", ascending=False)
fig = px.bar(pareto_df, x="Symbol", y="Risk Contribution %", title="Pareto Chart")
st.plotly_chart(fig, use_container_width=True)

st.header("Risk Metrics (Simulated)")
st.write("Portfolio Volatility (annualized): 15.7%")
st.write("Value at Risk (VaR, 95%): ₹18,740")
st.write("Sharpe Ratio: 1.12")
st.write("Maximum Drawdown: 5.2%")
st.write("Beta: 0.84")

st.header("Sample OHLC Chart (TCS)")
ohlc = pd.DataFrame({
    "Time": pd.date_range(start="09:30", periods=30, freq="5min"),
    "Open": np.linspace(3574, 3600, 30) + np.random.randn(30) * 10,
    "High": np.linspace(3575, 3605, 30) + np.random.rand(30) * 15,
    "Low": np.linspace(3570, 3592, 30) - np.random.rand(30) * 13,
    "Close": np.linspace(3574, 3590, 30) + np.random.randn(30) * 8,
    "Volume": np.random.randint(8000, 13000, 30)
})
fig = px.line(ohlc, x="Time", y="Close", title="TCS OHLC (Close)")
st.plotly_chart(fig, use_container_width=True)

st.write("More features and metrics can be added in a full version.")
