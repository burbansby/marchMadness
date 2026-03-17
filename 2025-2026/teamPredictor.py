import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import cross_val_score
from difflib import get_close_matches
import warnings
warnings.filterwarnings('ignore')

# ── CONFIG ────────────────────────────────────────────────────────────────────
HISTORICAL_PATH = "history.csv"
CURRENT_PATH    = "current.csv"
OUTPUT_PATH     = "predictions.csv"

# CONF_ENC is added via target encoding (mean wins per conf from training data)
FEATURES = ['ADJOE', 'ADJDE', 'BARTHAG', 'WAB', 'ADJ_T', 'CONF_ENC']

POSTSEASON_ORDER = {
    'R68': 0, 'R64': 1, 'R32': 2, 'S16': 3,
    'E8': 4,  'F4': 5,  '2ND': 6, 'Champions': 7
}
WINS_TO_ROUND = {v: k for k, v in POSTSEASON_ORDER.items()}

# ── 2026 TOURNAMENT TEAMS + SEEDS ─────────────────────────────────────────────
TOURNEY_2026 = {
    # Seed 1
    'Duke': 1, 'Arizona': 1, 'Michigan': 1, 'Florida': 1,
    # Seed 2
    'Houston': 2, 'Connecticut': 2, 'Iowa St.': 2, 'Purdue': 2,
    # Seed 3
    'Michigan St.': 3, 'Illinois': 3, 'Gonzaga': 3, 'Virginia': 3,
    # Seed 4
    'Nebraska': 4, 'Alabama': 4, 'Kansas': 4, 'Arkansas': 4,
    # Seed 5
    'Vanderbilt': 5, "St. John's": 5, 'Texas Tech': 5, 'Wisconsin': 5,
    # Seed 6
    'Tennessee': 6, 'North Carolina': 6, 'Louisville': 6, 'BYU': 6,
    # Seed 7
    'Kentucky': 7, "Saint Mary's": 7, 'Miami FL': 7, 'UCLA': 7,
    # Seed 8
    'Clemson': 8, 'Villanova': 8, 'Ohio St.': 8, 'Georgia': 8,
    # Seed 9
    'Utah St.': 9, 'TCU': 9, 'Saint Louis': 9, 'Iowa': 9,
    # Seed 10
    'Santa Clara': 10, 'UCF': 10, 'Missouri': 10, 'Texas A&M': 10,
    # Seed 11 (South Florida & VCU direct; NC State/Texas and SMU/Miami OH are First Four pairs)
    'South Florida': 11, 'VCU': 11, 'NC State': 11, 'Texas': 11, 'SMU': 11, 'Miami OH': 11,
    # Seed 12
    'Northern Iowa': 12, 'High Point': 12, 'McNeese': 12, 'Akron': 12,
    # Seed 13
    'Cal Baptist': 13, 'Hofstra': 13, 'Troy': 13, 'Hawaii': 13,
    # Seed 14
    'North Dakota St.': 14, 'Penn': 14, 'Kennesaw St.': 14, 'Wright St.': 14,
    # Seed 15
    'Furman': 15, 'Idaho': 15, 'Tennessee St.': 15, 'Queens': 15,
    # Seed 16 (Lehigh/Prairie View and UMBC/Howard are First Four pairs; Siena and LIU are direct)
    'Siena': 16, 'LIU': 16, 'Lehigh': 16, 'Prairie View': 16, 'UMBC': 16, 'Howard': 16,
}

# ── LOAD HISTORY ──────────────────────────────────────────────────────────────
hist = pd.read_csv(HISTORICAL_PATH)
hist = hist[hist['POSTSEASON'].notna() & hist['POSTSEASON'].isin(POSTSEASON_ORDER)]
hist['WINS'] = hist['POSTSEASON'].map(POSTSEASON_ORDER)
hist['CONF'] = hist['CONF'].str.strip()

# ── CONFERENCE TARGET ENCODING ────────────────────────────────────────────────
# Mean wins per conf with smoothing: pulls low-sample confs toward global mean.
# k=5 means a conf needs >5 tourney appearances before its mean dominates.
SMOOTH_K    = 5
global_mean = hist['WINS'].mean()
conf_stats  = hist.groupby('CONF')['WINS'].agg(['sum', 'count'])
conf_enc    = ((conf_stats['sum'] + global_mean * SMOOTH_K) /
               (conf_stats['count'] + SMOOTH_K)).to_dict()

hist['CONF_ENC'] = hist['CONF'].map(conf_enc).fillna(global_mean)

print("Conference strength (avg tournament wins, smoothed):")
print(pd.Series(conf_enc).sort_values(ascending=False).round(3).to_string())
print()

BASE_FEATURES = ['ADJOE', 'ADJDE', 'BARTHAG', 'WAB', 'ADJ_T']
hist = hist.dropna(subset=BASE_FEATURES)

X_train = hist[FEATURES]
y_train = hist['WINS']
print(f"Training on {len(X_train)} team-seasons  |  years: {hist['YEAR'].min()}–{hist['YEAR'].max()}")
print(f"Win distribution: {dict(y_train.value_counts().sort_index())}\n")

# ── TRAIN ─────────────────────────────────────────────────────────────────────
base = GradientBoostingClassifier(
    n_estimators=300, learning_rate=0.05,
    max_depth=4, subsample=0.8, random_state=42
)
model = CalibratedClassifierCV(base, cv=5, method='isotonic')
model.fit(X_train, y_train)

cv = cross_val_score(base, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')
print(f"Cross-val MAE: {-cv.mean():.3f} ± {cv.std():.3f} wins\n")

# ── LOAD CURRENT YEAR ─────────────────────────────────────────────────────────
curr_raw = pd.read_csv(CURRENT_PATH)
curr_raw.columns = curr_raw.columns.str.strip().str.lower()
curr_raw = curr_raw.rename(columns={
    'team': 'TEAM', 'conf': 'CONF', 'adjoe': 'ADJOE',
    'adjde': 'ADJDE', 'barthag': 'BARTHAG', 'wab': 'WAB', 'adjt': 'ADJ_T',
})
curr_raw['CONF'] = curr_raw['CONF'].str.strip()

# Apply encoding learned from training — unseen confs fall back to global mean
curr_raw['CONF_ENC'] = curr_raw['CONF'].map(conf_enc).fillna(global_mean)

print(f"Loaded {len(curr_raw)} teams from {CURRENT_PATH}")

# ── MATCH TO TOURNAMENT FIELD ─────────────────────────────────────────────────
csv_teams = curr_raw['TEAM'].tolist()

rows, unmatched = [], []
for tourney_name, seed in TOURNEY_2026.items():
    match = tourney_name if tourney_name in csv_teams else \
            next(iter(get_close_matches(tourney_name, csv_teams, n=1, cutoff=0.7)), None)
    if match:
        row = curr_raw[curr_raw['TEAM'] == match].iloc[0].copy()
        row['TEAM'] = tourney_name
        row['SEED'] = seed
        rows.append(row)
    else:
        unmatched.append(tourney_name)

curr = pd.DataFrame(rows).reset_index(drop=True)

print(f"Matched {len(curr)}/68 tournament teams")
if unmatched:
    print(f"\nUnmatched — adjust spellings in TOURNEY_2026:\n  {sorted(unmatched)}\n")
else:
    print("All tournament teams matched\n")

# ── PREDICT ───────────────────────────────────────────────────────────────────
curr_feat = curr.dropna(subset=BASE_FEATURES).copy()
X_curr    = curr_feat[FEATURES]
classes   = model.classes_
proba     = model.predict_proba(X_curr)

expected_wins  = (proba * classes).sum(axis=1)
predicted_wins = classes[proba.argmax(axis=1)]

def confidence_pct(row, exp, cls):
    return sum(p for p, c in zip(row, cls) if abs(c - exp) <= 1)

confidences = [confidence_pct(proba[i], expected_wins[i], classes) for i in range(len(curr_feat))]

# ── OUTPUT ────────────────────────────────────────────────────────────────────
out = curr_feat[['TEAM', 'CONF', 'SEED', 'ADJOE', 'ADJDE', 'BARTHAG', 'WAB', 'CONF_ENC']].copy()
out = out.rename(columns={'CONF_ENC': 'CONF_STRENGTH'})
out['CONF_STRENGTH']   = out['CONF_STRENGTH'].round(3)

out['EXPECTED_WINS']   = expected_wins.round(2)

out['CONFIDENCE']      = [f"{c:.1%}" for c in confidences]

for i, cls in enumerate(classes):
    label = WINS_TO_ROUND.get(cls, str(cls))
    out[f'P({label})'] = (proba[:, i] * 100).round(1)

out = out.sort_values('EXPECTED_WINS', ascending=False).reset_index(drop=True)
out.to_csv(OUTPUT_PATH, index=False)

print(f"Saved → {OUTPUT_PATH}\n")
print(out[['TEAM', 'CONF', 'SEED', 'CONF_STRENGTH', 'EXPECTED_WINS', 'CONFIDENCE']].to_string(index=False))