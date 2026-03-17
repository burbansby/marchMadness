import pandas as pd
import numpy as np
import random

PREDICTIONS_PATH = "predictions.csv"

# ── BRACKET STRUCTURE ─────────────────────────────────────────────────────────
# Each region is a list of (seed, team_name) in standard bracket order.
# Games pair index 0v7, 1v6, 2v5, 3v4 in each half.
# First Four play-in results are represented as tuples — one team is picked
# before the main bracket simulation begins.

BRACKET = {
    "East": [
        (1,  "Duke"),
        (8,  "Ohio St."),
        (5,  "St. John's"),
        (4,  "Kansas"),
        (6,  "Louisville"),
        (3,  "Michigan St."),
        (7,  "UCLA"),
        (2,  "Connecticut"),
        # opponents
        (16, "Siena"),
        (9,  "TCU"),
        (12, "Northern Iowa"),
        (13, "Cal Baptist"),
        (11, "South Florida"),
        (14, "North Dakota St."),
        (10, "UCF"),
        (15, "Furman"),
    ],
    "South": [
        (1,  "Florida"),
        (8,  "Clemson"),
        (5,  "Vanderbilt"),
        (4,  "Nebraska"),
        (6,  "North Carolina"),
        (3,  "Illinois"),
        (7,  "Saint Mary's"),
        (2,  "Houston"),
        # opponents
        (16, "PLAY_IN_16S"),   # Lehigh vs Prairie View winner
        (9,  "Iowa"),
        (12, "McNeese"),
        (13, "Troy"),
        (11, "VCU"),
        (14, "Penn"),
        (10, "Texas A&M"),
        (15, "Idaho"),
    ],
    "Midwest": [
        (1,  "Michigan"),
        (8,  "Georgia"),
        (5,  "Texas Tech"),
        (4,  "Alabama"),
        (6,  "Tennessee"),
        (3,  "Virginia"),
        (7,  "Kentucky"),
        (2,  "Iowa St."),
        # opponents
        (16, "PLAY_IN_16M"),   # UMBC vs Howard winner
        (9,  "Saint Louis"),
        (12, "Akron"),
        (13, "Hofstra"),
        (11, "PLAY_IN_11M"),   # SMU vs Miami OH winner
        (14, "Wright St."),
        (10, "Santa Clara"),
        (15, "Tennessee St."),
    ],
    "West": [
        (1,  "Arizona"),
        (8,  "Villanova"),
        (5,  "Wisconsin"),
        (4,  "Arkansas"),
        (6,  "BYU"),
        (3,  "Gonzaga"),
        (7,  "Miami FL"),
        (2,  "Purdue"),
        # opponents
        (16, "LIU"),
        (9,  "Utah St."),
        (12, "High Point"),
        (13, "Hawaii"),
        (11, "PLAY_IN_11W"),   # NC State vs Texas winner
        (14, "Kennesaw St."),
        (10, "Missouri"),
        (15, "Queens"),
    ],
}

FIRST_FOUR = [
    ("Lehigh",   "Prairie View",  "PLAY_IN_16S"),
    ("UMBC",     "Howard",        "PLAY_IN_16M"),
    ("SMU",      "Miami OH",      "PLAY_IN_11M"),
    ("NC State", "Texas",         "PLAY_IN_11W"),
]

# ── LOAD PREDICTIONS ──────────────────────────────────────────────────────────
df = pd.read_csv(PREDICTIONS_PATH)
strength = dict(zip(df["TEAM"], df["BARTHAG"]))

def get_strength(team):
    """Return BARTHAG strength; default to 0.5 for any unrecognised team."""
    return strength.get(team, 0.5)

def win_prob(teamA, teamB):
    """
    Log-odds win probability using BARTHAG.
    BARTHAG is a probability (P of beating avg D1 team). Converting to log-odds
    before differencing correctly amplifies gaps — raw Bradley-Terry (a/(a+b))
    compresses everything toward 50%, giving a 1-seed only ~68% vs a 16-seed
    instead of the realistic ~98%.
    """
    a = np.clip(get_strength(teamA), 1e-6, 1 - 1e-6)
    b = np.clip(get_strength(teamB), 1e-6, 1 - 1e-6)
    lo_a = np.log(a / (1 - a))
    lo_b = np.log(b / (1 - b))
    return 1 / (1 + np.exp(-(lo_a - lo_b)))

def simulate_game(teamA, teamB):
    """Return winner of a single game."""
    return teamA if random.random() < win_prob(teamA, teamB) else teamB

# ── FIRST FOUR ────────────────────────────────────────────────────────────────
def run_first_four():
    results = {}
    for t1, t2, slot in FIRST_FOUR:
        winner = simulate_game(t1, t2)
        results[slot] = winner
    return results

# ── REGION SIMULATION ─────────────────────────────────────────────────────────
def resolve_region(region_slots, playin_map):
    """Replace PLAY_IN placeholders, then simulate 4 rounds."""
    teams = []
    for seed, name in region_slots:
        teams.append((seed, playin_map.get(name, name)))

    # Standard bracket order: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
    top_half    = teams[:8]     # seeds 1,8,5,4,6,3,7,2
    bottom_half = teams[8:]     # seeds 16,9,12,13,11,14,10,15

    # Pair them: top[i] vs bottom[i]
    round1 = [(t[1], b[1]) for t, b in zip(top_half, bottom_half)]

    def play_round(matchups):
        return [simulate_game(a, b) for a, b in matchups]

    def pair_winners(winners):
        return [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]

    r1_winners = play_round(round1)
    r2_winners = play_round(pair_winners(r1_winners))
    r3_winners = play_round(pair_winners(r2_winners))  # Sweet 16
    r4_winners = play_round(pair_winners(r3_winners))  # Elite 8 → region champ

    return {
        "R64":  r1_winners,
        "R32":  r2_winners,
        "S16":  r3_winners,
        "E8":   r4_winners,
        "champ": r4_winners[0],
    }

# ── FULL TOURNAMENT ───────────────────────────────────────────────────────────
def simulate_tournament():
    playin = run_first_four()
    regions = {}
    for name, slots in BRACKET.items():
        regions[name] = resolve_region(slots, playin)

    # Final Four
    east_champ    = regions["East"]["champ"]
    west_champ    = regions["West"]["champ"]
    south_champ   = regions["South"]["champ"]
    midwest_champ = regions["Midwest"]["champ"]

    sf1 = simulate_game(east_champ, south_champ)
    sf2 = simulate_game(west_champ, midwest_champ)
    champion = simulate_game(sf1, sf2)

    return regions, playin, (east_champ, south_champ, sf1), (west_champ, midwest_champ, sf2), champion

# ── DISPLAY ───────────────────────────────────────────────────────────────────
def seed_of(team, playin_map):
    for region_slots in BRACKET.values():
        for seed, name in region_slots:
            resolved = playin_map.get(name, name)
            if resolved == team:
                return seed
    return "?"

def fmt(team, playin_map):
    s = seed_of(team, playin_map)
    return f"({s}) {team}"

def print_bracket(regions, playin, ff_east, ff_south, champion):
    print("\n" + "="*65)
    print(f"{'2026 NCAA TOURNAMENT SIMULATION':^65}")
    print("="*65)

    for region_name, res in regions.items():
        print(f"\n{'─'*65}")
        print(f"  {region_name.upper()} REGION")
        print(f"{'─'*65}")
        label_w = 32
        print(f"  {'ROUND OF 64':<{label_w}} {'ROUND OF 32'}")
        for i, (r64, r32) in enumerate(zip(res["R64"], res["R32"])):
            # each R32 winner came from a pair of R64 winners
            pass

        # Print round by round
        rounds = [
            ("Round of 64",  res["R64"]),
            ("Round of 32",  res["R32"]),
            ("Sweet 16",     res["S16"]),
            ("Elite 8",      res["E8"]),
        ]
        for label, winners in rounds:
            names = "  |  ".join([fmt(t, playin) for t in winners])
            print(f"  {label:<14} → {names}")

    print(f"\n{'='*65}")
    print(f"  FINAL FOUR")
    print(f"  East:    {fmt(ff_east[0], playin)}  vs  {fmt(ff_east[1], playin)}")
    print(f"           → {fmt(ff_east[2], playin)} advances")
    print(f"  South:   {fmt(ff_south[0], playin)}  vs  {fmt(ff_south[1], playin)}")
    print(f"           → {fmt(ff_south[2], playin)} advances")
    print(f"\n  CHAMPIONSHIP")
    print(f"  {fmt(ff_east[2], playin)}  vs  {fmt(ff_south[2], playin)}")
    print(f"\n{'★'*65}")
    print(f"  🏆  CHAMPION: {fmt(champion, playin)}")
    print(f"{'★'*65}\n")

    print("  FIRST FOUR RESULTS:")
    for t1, t2, slot in FIRST_FOUR:
        winner = playin[slot]
        loser  = t2 if winner == t1 else t1
        print(f"  {t1} vs {t2} → {winner} advances")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    random.seed()   # true random each run
    regions, playin, ff_east, ff_south, champion = simulate_tournament()
    print_bracket(regions, playin, ff_east, ff_south, champion)