import yfinance as yf
import pandas as pd
import numpy as np
from config import LOOKBACK_DAYS

def compute_ranking(tickers):

    data = yf.download(tickers, period="1y", progress=False)["Close"]

    returns = data.pct_change().dropna()

    momentum = data.iloc[-1] / data.iloc[-LOOKBACK_DAYS] - 1
    volatility = returns.std() * np.sqrt(252)

    quant_score = momentum / volatility

    df = pd.DataFrame({
        "quant_score": quant_score
    }).sort_values("quant_score", ascending=False)

    return df