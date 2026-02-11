import pandas as pd
import yfinance as yf

def analyze_portfolio_csv(uploaded_file):

    df = pd.read_csv(uploaded_file)

    df["Ticker"] = df["Ticker"].str.upper()

    prices = yf.download(df["Ticker"].tolist(), period="1y", progress=False)["Close"]
    latest_prices = prices.iloc[-1]

    df["Current Price"] = df["Ticker"].map(latest_prices)
    df["Market Value"] = df["Quantity"] * df["Current Price"]
    df["Total Cost"] = df["Quantity"] * df["Cost Per Share"]
    df["PnL"] = df["Market Value"] - df["Total Cost"]
    df["PnL %"] = df["PnL"] / df["Total Cost"]

    return df.sort_values("PnL %", ascending=False)
