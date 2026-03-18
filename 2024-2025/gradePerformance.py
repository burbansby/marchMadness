import pandas as pd
import numpy as np

# --- Load data ---
preds = pd.read_csv("TeamPredictions.csv")
outcomes = pd.read_csv("TeamOutcomes.csv")
outcomes.columns = outcomes.columns.str.strip()

df = preds.merge(outcomes, on="Team")
df.rename(columns={"Wins": "Predicted", "Dev": "StdDev", "Outcome": "Actual"}, inplace=True)

# --- Core metrics ---
df["Error"]         = df["Actual"] - df["Predicted"]
df["AbsError"]      = df["Error"].abs()
df["ZScore"]        = df["Error"] / df["StdDev"]
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
    if s <= 4:   return "1–4 (favorites)"
    if s <= 8:   return "5–8 (mid-high)"
    if s <= 12:  return "9–12 (mid-low)"
    return "13–16 (underdogs)"

df["SeedGroup"] = df["Seed"].apply(seed_bucket)
by_seed = df.groupby("SeedGroup").agg(
    Teams         = ("Team", "count"),
    MAE           = ("AbsError", "mean"),
    Bias          = ("Error", "mean"),
    Within1Sigma  = ("WithinOneSigma", "mean"),
).round(3)

# --- Surprises / Busts ---
surprises = df.nlargest(5, "ZScore")[["Team", "Seed", "Predicted", "StdDev", "Actual", "ZScore"]].copy()
busts     = df.nsmallest(5, "ZScore")[["Team", "Seed", "Predicted", "StdDev", "Actual", "ZScore"]].copy()

# --- Full breakdown ---
report_cols = ["Team", "Seed", "Region", "Predicted", "StdDev", "Actual", "Error", "ZScore", "WithinOneSigma"]
report = df.sort_values("AbsError", ascending=False)[report_cols].copy()

# --- Helpers ---
def fmt_df(dataframe, float_cols=None, bool_cols=None):
    df2 = dataframe.copy()
    if float_cols:
        for col in float_cols:
            if col in df2.columns:
                df2[col] = df2[col].map(lambda x: f"{x:.3f}")
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

lines.append("# March Madness Prediction Report — 2024–25\n")

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
with open(out_path, "w") as f:
    f.write(md_output)

print(f"Written to {out_path}")