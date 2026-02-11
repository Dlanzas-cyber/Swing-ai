def apply_ai_adjustment(ranking_df, ai_result):

    adjustments = ai_result.get("swing_bias_adjustment", {})
    confidence = ai_result.get("confidence", 0)

    ranking_df["ai_adjustment"] = ranking_df.index.map(
        lambda x: adjustments.get(x, 0)
    )

    ranking_df["hybrid_score"] = (
        0.7 * ranking_df["quant_score"] +
        0.3 * confidence +
        ranking_df["ai_adjustment"]
    )

    return ranking_df.sort_values("hybrid_score", ascending=False)
