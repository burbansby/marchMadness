import pandas as pd
import numpy as np

# --- Load data ---
# The 2025-26 predictions are stored as an exit-round probability distribution
# rather than a precomputed Wins/Dev pair like last year. We derive the
# predicted wins and standard deviation from that distribution so the grader
# mirrors the 2024-25 version.
preds = pd.read_csv("predictions.csv")
outcomes = pd.read_csv("TeamOutcomes.csv")
outcomes.columns = outcomes.columns.str.strip()

# Map each "eliminated in round X" probability column to the number of
# tournament wins that outcome represents, on the SAME scale the manual
# outcomes use (champion = 6, runner-up = 5, ... first-round loss = 0).
# A First Four (R68) appearance and a Round-of-64 loss both count as 0 wins.
ROUND_WINS = {
    "P(R68)": 0,
    "P(R64)": 0,
    "P(R32)": 1,
    "P(S16)": 2,
    "P(E8)": 3,
    "P(F4)": 4,
    "P(2ND)": 5,
    "P(Champions)": 6,
}

prob_cols = list(ROUND_WINS.keys())
wins_vec = np.array([ROUND_WINS[c] for c in prob_cols], dtype=float)

# Probabilities are stored as percentages; normalize each row to sum to 1.
probs = preds[prob_cols].to_numpy(dtype=float)
row_sums = probs.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1.0
probs = probs / row_sums

predicted = probs @ wins_vec
ex2 = probs @ (wins_vec ** 2)
variance = np.clip(ex2 - predicted ** 2, 0, None)
stddev = np.sqrt(variance)

preds = preds.rename(columns={"TEAM": "Team", "SEED": "Seed", "CONF": "Conf"})
preds["Predicted"] = predicted
preds["StdDev"] = stddev

# Cumulative "reach round" probabilities (model's chance of >= N tournament wins),
# derived from the same exit-round distribution. Index k in prob_cols carries
# wins_vec[k] wins, so P(reach >= n) sums every column worth at least n wins.
for n in range(1, 7):
    mask = wins_vec >= n
    preds[f"PReach{n}"] = (probs[:, mask].sum(axis=1)) * 100.0

# Model's championship probability (%) and a parsed confidence score.
preds["PChamp"] = preds["P(Champions)"]
preds["Confidence"] = (
    preds["CONFIDENCE"].astype(str).str.replace("%", "", regex=False).astype(float)
)

keep = ["Team", "Seed", "Conf", "Predicted", "StdDev", "PChamp", "Confidence"] + \
       [f"PReach{n}" for n in range(1, 7)]
df = preds[keep].merge(outcomes, on="Team")
df.rename(columns={"Outcome": "Actual"}, inplace=True)

# --- Core metrics ---
# Guard against zero std dev when computing z-scores.
safe_std = df["StdDev"].replace(0, np.nan)

df["Error"]         = df["Actual"] - df["Predicted"]
df["AbsError"]      = df["Error"].abs()
df["ZScore"]        = df["Error"] / safe_std
df["WithinOneSigma"]= df["AbsError"] <= df["StdDev"]
df["WithinTwoSigma"]= df["AbsError"] <= 2 * df["StdDev"]

mae  = df["AbsError"].mean()
rmse = np.sqrt((df["Error"] ** 2).mean())
bias = df["Error"].mean()
r    = df[["Predicted", "Actual"]].corr().iloc[0, 1]
within_1s    = df["WithinOneSigma"].mean() * 100
within_2s    = df["WithinTwoSigma"].mean() * 100
mean_abs_z   = df["ZScore"].abs().mean()

# --- Seed-group breakdown ---
def seed_bucket(s):
    if s <= 4:   return "1-4 (favorites)"
    if s <= 8:   return "5-8 (mid-high)"
    if s <= 12:  return "9-12 (mid-low)"
    return "13-16 (underdogs)"

df["SeedGroup"] = df["Seed"].apply(seed_bucket)
by_seed = df.groupby("SeedGroup").agg(
    Teams         = ("Team", "count"),
    MAE           = ("AbsError", "mean"),
    Bias          = ("Error", "mean"),
    Within1Sigma  = ("WithinOneSigma", "mean"),
).round(3)

# --- Conference performance ---
by_conf = df.groupby("Conf").agg(
    Teams      = ("Team", "count"),
    PredWins   = ("Predicted", "sum"),
    ActualWins = ("Actual", "sum"),
    MAE        = ("AbsError", "mean"),
).round(2)
by_conf["Diff"] = (by_conf["ActualWins"] - by_conf["PredWins"]).round(2)
by_conf = by_conf.sort_values("ActualWins", ascending=False)

# --- Round-reach calibration ---
# For each round threshold, compare the model's expected number of teams to
# reach it (sum of reach probabilities) against how many actually did.
round_labels = {
    1: "Round of 32 (≥1 win)",
    2: "Sweet 16 (≥2 wins)",
    3: "Elite 8 (≥3 wins)",
    4: "Final 4 (≥4 wins)",
    5: "Title game (≥5 wins)",
    6: "Champion (≥6 wins)",
}
calib_rows = []
for n in range(1, 7):
    expected = df[f"PReach{n}"].sum() / 100.0
    actual = int((df["Actual"] >= n).sum())
    calib_rows.append({
        "Round": round_labels[n],
        "Expected": round(expected, 1),
        "Actual": actual,
        "Diff": round(actual - expected, 1),
    })
calibration = pd.DataFrame(calib_rows)

# --- Championship & deep-run forecast ---
# The model's per-team exit distributions each sum to ~100%, but they are not
# jointly normalized across the field: the raw P(Champions) column sums to far
# more than 100% (there can only be one champion). Rescale it into true title
# odds that sum to 100% before treating it as a championship probability.
raw_champ_total = df["PChamp"].sum()
df["TitleOdds"] = df["PChamp"] / raw_champ_total * 100.0

champ_idx = df["Actual"].idxmax()
champion = df.loc[champ_idx, "Team"]
model_pick = df.loc[df["TitleOdds"].idxmax(), "Team"]
df["IsChamp"] = (df.index == champ_idx).astype(int)
brier_champ = ((df["TitleOdds"] / 100.0 - df["IsChamp"]) ** 2).mean()
# Final-Four Brier: scored as 68 independent "did they reach ≥4 wins" predictions,
# so this one does not need cross-field normalization.
made_f4 = (df["Actual"] >= 4).astype(int)
brier_f4 = ((df["PReach4"] / 100.0 - made_f4) ** 2).mean()
title_contenders = df.nlargest(8, "TitleOdds")[
    ["Team", "Seed", "TitleOdds", "Actual"]
].copy()

# --- Confidence vs accuracy ---
conf_corr = df[["Confidence", "AbsError"]].corr().iloc[0, 1]
conf_bins = [0, 40, 60, 80, 101]
conf_labels = ["<40%", "40–60%", "60–80%", "80%+"]
df["ConfBucket"] = pd.cut(df["Confidence"], bins=conf_bins, labels=conf_labels, right=False)
by_conf_bucket = df.groupby("ConfBucket", observed=True).agg(
    Teams = ("Team", "count"),
    MAE   = ("AbsError", "mean"),
    Bias  = ("Error", "mean"),
).round(3)

# --- Cinderellas & chalk busts ---
cinderellas = df[df["Seed"] >= 10].nlargest(5, "Actual")[
    ["Team", "Seed", "Conf", "Predicted", "Actual", "Error"]
].copy()
chalk_busts = df[df["Seed"] <= 4].nsmallest(5, "Actual")[
    ["Team", "Seed", "Conf", "Predicted", "Actual", "Error"]
].copy()

# --- Surprises / Busts ---
surprises = df.nlargest(5, "ZScore")[["Team", "Seed", "Predicted", "StdDev", "Actual", "ZScore"]].copy()
busts     = df.nsmallest(5, "ZScore")[["Team", "Seed", "Predicted", "StdDev", "Actual", "ZScore"]].copy()

# --- Full breakdown ---
report_cols = ["Team", "Seed", "Conf", "Predicted", "StdDev", "Actual", "Error", "ZScore", "WithinOneSigma"]
report = df.sort_values("AbsError", ascending=False)[report_cols].copy()

# --- Helpers ---
def fmt_df(dataframe, float_cols=None, bool_cols=None):
    df2 = dataframe.copy()
    if float_cols:
        for col in float_cols:
            if col in df2.columns:
                df2[col] = df2[col].map(lambda x: f"{x:.3f}" if pd.notna(x) else "—")
    if bool_cols:
        for col in bool_cols:
            if col in df2.columns:
                df2[col] = df2[col].map(lambda x: "✓" if x else "✗")
    return df2

def df_to_md(dataframe):
    cols = list(dataframe.columns)
    header = "| " + " | ".join(cols) + " |"
    sep    = "| " + " | ".join(["---"] * len(cols)) + " |"
    rows   = []
    for _, row in dataframe.iterrows():
        rows.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join([header, sep] + rows)

# --- Build markdown ---
lines = []

lines.append("# March Madness Prediction Report — 2025–26\n")

lines.append("## Overall Accuracy\n")
lines.append(f"| Metric | Value |")
lines.append(f"| --- | --- |")
lines.append(f"| MAE (mean abs error) | {mae:.3f} wins |")
lines.append(f"| RMSE | {rmse:.3f} wins |")
lines.append(f"| Bias (actual − predicted) | {bias:+.3f} ({'model undershot' if bias > 0 else 'model overshot'}) |")
lines.append(f"| Correlation (r) | {r:.3f} |")
lines.append("")

lines.append("## Coverage\n")
lines.append(f"| Metric | Value | Ideal |")
lines.append(f"| --- | --- | --- |")
lines.append(f"| Within ±1 std dev | {within_1s:.1f}% | ~68% |")
lines.append(f"| Within ±2 std devs | {within_2s:.1f}% | ~95% |")
lines.append(f"| Mean |Z-score| | {mean_abs_z:.2f} | ~0.80 |")
lines.append("")

lines.append("## Results by Seed Group\n")
seed_fmt = fmt_df(by_seed, float_cols=["MAE", "Bias", "Within1Sigma"])
lines.append(df_to_md(seed_fmt.reset_index()))
lines.append("")

lines.append("## Championship & Deep-Run Forecast\n")
lines.append(f"- **Model's title pick:** {model_pick} ({df.loc[df['TitleOdds'].idxmax(), 'TitleOdds']:.1f}% to win it all)")
lines.append(f"- **Actual champion:** {champion} ({int(df.loc[champ_idx, 'Actual'])} wins)")
lines.append(f"- **Champion Brier score:** {brier_champ:.4f} (lower is better)")
lines.append(f"- **Final-4 Brier score:** {brier_f4:.4f}")
lines.append("")
lines.append(f"> Title odds are rescaled to sum to 100% across the field. The model's raw "
             f"`P(Champions)` column sums to {raw_champ_total:.0f}% — its per-team distributions "
             f"are not jointly normalized, so it over-allocates championship share (and deep runs "
             f"generally; see calibration below).\n")
lines.append("Model's top title contenders (normalized odds) vs. how they finished:\n")
tc_fmt = fmt_df(title_contenders, float_cols=["TitleOdds"])
lines.append(df_to_md(tc_fmt))
lines.append("")

lines.append("## Round-Reach Calibration\n")
lines.append("Expected = model's projected number of teams to reach each round; Actual = how many did.\n")
lines.append(df_to_md(calibration))
lines.append("")

lines.append("## Conference Performance\n")
conf_fmt = fmt_df(by_conf.reset_index(), float_cols=["PredWins", "ActualWins", "MAE", "Diff"])
lines.append(df_to_md(conf_fmt))
lines.append("")

lines.append("## Confidence vs. Accuracy\n")
lines.append(f"Correlation between model confidence and absolute error: **{conf_corr:+.3f}** "
             f"({'higher confidence → lower error' if conf_corr < 0 else 'higher confidence → higher error'}).\n")
cb_fmt = fmt_df(by_conf_bucket.reset_index(), float_cols=["MAE", "Bias"])
lines.append(df_to_md(cb_fmt))
lines.append("")

lines.append("## Cinderellas (Double-Digit Seeds, Most Wins)\n")
cind_fmt = fmt_df(cinderellas, float_cols=["Predicted", "Error"])
lines.append(df_to_md(cind_fmt))
lines.append("")

lines.append("## Chalk Busts (Top-4 Seeds, Fewest Wins)\n")
chalk_fmt = fmt_df(chalk_busts, float_cols=["Predicted", "Error"])
lines.append(df_to_md(chalk_fmt))
lines.append("")

lines.append("## Biggest Upsets (Actual >> Predicted)\n")
surp_fmt = fmt_df(surprises, float_cols=["Predicted", "StdDev", "ZScore"])
lines.append(df_to_md(surp_fmt))
lines.append("")

lines.append("## Biggest Busts (Actual << Predicted)\n")
bust_fmt = fmt_df(busts, float_cols=["Predicted", "StdDev", "ZScore"])
lines.append(df_to_md(bust_fmt))
lines.append("")

lines.append("## Full Team Breakdown\n")
rep_fmt = fmt_df(report, float_cols=["Predicted", "StdDev", "Error", "ZScore"], bool_cols=["WithinOneSigma"])
lines.append(df_to_md(rep_fmt))
lines.append("")

md_output = "\n".join(lines)

out_path = "performance.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(md_output)

print(f"Written to {out_path}")
