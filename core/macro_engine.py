import yfinance as yf

def get_macro_context():

    spy = yf.download("SPY", period="6mo", progress=False)["Close"]
    vix = yf.download("^VIX", period="6mo", progress=False)["Close"]

    spy_trend = "uptrend" if spy.iloc[-1] > spy.mean() else "downtrend"
    vix_level = float(vix.iloc[-1])

    return {
        "spy_trend": spy_trend,
        "vix_level": vix_level
    }