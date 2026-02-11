import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(ranking_df, portfolio_df, macro_dict):

    macro_text = f"""
SPY trend: {macro_dict['spy_trend']}
VIX level: {macro_dict['vix_level']}
"""

    prompt = f"""
You are a systematic macro trading model.

Macro:
{macro_text}

Top Quant Ranking:
{ranking_df.head(5).to_string()}

Portfolio Snapshot:
{portfolio_df.to_string() if portfolio_df is not None else "No portfolio uploaded"}

Rules:
- Do NOT calculate indicators.
- Bias adjustment between -0.2 and +0.2.
- Confidence between 0 and 1.
- Return ONLY valid JSON.

Format:
{{
 "macro_regime": "",
 "confidence": 0.0,
 "swing_bias_adjustment": {{
    "TICKER": 0.0
 }},
 "portfolio_best_additions_this_month": [],
 "summary": ""
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)

