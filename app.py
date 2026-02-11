import streamlit as st
from config import DEFAULT_UNIVERSE, TOP_N
from core.ranking_engine import compute_ranking
from core.macro_engine import get_macro_context
from core.portfolio_engine import analyze_portfolio_csv
from core.groq_ai import call_groq
from core.hybrid_engine import apply_ai_adjustment
from core.cache import get_today_cache, store_today

st.title("Swing Trading AI Hybrid System")

universe_input = st.text_input(
    "Universe (comma separated)",
    ",".join(DEFAULT_UNIVERSE)
)

tickers = [t.strip().upper() for t in universe_input.split(",")]

ranking_df = compute_ranking(tickers)

st.subheader("Quant Ranking")
st.dataframe(ranking_df)

portfolio_file = st.file_uploader("Upload Portfolio CSV", type=["csv"])

portfolio_df = None
if portfolio_file:
    portfolio_df = analyze_portfolio_csv(portfolio_file)
    st.subheader("Portfolio Analysis")
    st.dataframe(portfolio_df)

macro_dict = get_macro_context()
st.write("Macro Context:", macro_dict)

cached = get_today_cache()

if cached:
    ai_result = cached
else:
    ai_result = call_groq(ranking_df, portfolio_df, macro_dict)
    store_today(ai_result)

st.subheader("AI Output")
st.json(ai_result)

hybrid_df = apply_ai_adjustment(ranking_df, ai_result)

st.subheader("Hybrid Ranking")
st.dataframe(hybrid_df.head(TOP_N))
