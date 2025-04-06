import pandas as pd
import random
import itertools
import statistics
from pandasgui import show
import time
import math

current_year = 2025
trials = 30
max_time = 60*60
knn_runtime = 7
k_range = (1,15)
weight_max = 5
training_split_size = .1
rank_fields = [
    "Seed",
    "Net Rating Rank",
    "Adjusted Tempo Rank",
    "Adjusted Offensive Efficiency Rank",
    "Adjusted Defensive Efficiency Rank",
    "RankeFGPct",
    "RankTOPct",
    "RankORPct",
    "RankFTRate",
    "RankOff3PtFG",
    "RankAvgHeight",
    "RankExperience",
    "BenchRank",
]
important_stuff = [
        "Team",
        "Year",
        "Short Conference Name",
        "Current Coach",
        "Post-Season Tournament",
        "Region",
    ]
important_stuff += rank_fields

def min2sec(x):
    return x*60

def generate_configs(max, max_trial_time):
    combinations = []
    while len(combinations)*knn_runtime < max_trial_time: 
        input_dict = {}
        for elm in important_stuff:
            if elm not in ["Year","Post-Season Tournament"]:
                input_dict[elm] = random.randint(0,max)
        combinations.append(input_dict)
    
    return combinations

def convert_placement(x):
    if x == 68:
        return -1
    if x == 64:
        return 0
    if x == 32:
        return 1
    if x == 16:
        return 2
    if x == 8:
        return 3
    if x == 4:
        return 4
    if x == 2:
        return 5
    if x == 1:
        return 6
    return None

   
def loadData():
    # Load CSV
    csv_file_path = 'DEV _ March Madness.csv'
    df = pd.read_csv(csv_file_path)
    
    # Remove garbage cols
    df = df[important_stuff]

    # Get only 2010 onward (minus 2020/2021)
    df = df[df['Year'] >= 2010]
    df = df[df['Year'] != 2020]
    df = df[df['Year'] != 2021]
    
    # Remove non tourney teams
    df = df[df['Post-Season Tournament'] == 'March Madness']

    # Split by historical and this year
    current = df[df['Year'] == current_year]
    df = df[df['Year'] != current_year] 

    # Add outcomes to the historical
    resumes = pd.read_csv("Resumes.csv")
    df = pd.merge(df, resumes[['Team', 'Year', 'ROUND']], on=['Team', 'Year'], how='left')
    df['Wins'] = df['ROUND'].apply(lambda x: convert_placement(x))
    df.insert(4,'Wins', df.pop('Wins'))
    df = df.drop(columns=["ROUND"])

    
    return df,current

def get_rank_sim(field, x, y):
    max = 375
    if field == "Net Rating Rank":
        max = 7250
    if field == "Seed":
        max = 16
    diff = abs(int(x)-int(y))
    return (max-diff)/max


def get_team_similarity(team, cmp, weights):
    scores = []
    for field, val in team.items():
        if field in [ "Team","Short Conference Name", "Current Coach"]:
            if val == cmp[field]:
                scores.append(weights[field]**2)
        if field in rank_fields:
            scores.append(get_rank_sim(field, val, cmp[field])**2)
    return sum(scores)**.5

def find_neighbors(team, data, weights):
    neighbors = []
    for _,cmp in data.iterrows():
        sim = get_team_similarity(team, cmp, weights)
        neighbors.append((sim, cmp))
    neighbors.sort(reverse=True, key=lambda x:x[0])
    return neighbors


def get_win_pred(team, k, weights=None, ref=None, training=None):
    tid = team['Team'] + str(team['Year'])
    if ref == None:
        ref = {}
        ref[tid] = find_neighbors(team, training, weights)
    
    neigbors = ref[tid][:k]
    nwins = []
    for _,n in neigbors:
        nwins.append(n['Wins'])
    if k == 1:
        mean = nwins[0]
        std_dev = 1
    else:
        mean = statistics.mean(nwins)
        std_dev = statistics.stdev(nwins)
    return mean, std_dev
    


def find_best_k(training, test, K_range, weights):
    size = test.shape[0]
    ks = {}
    ref = {}
    for _,team in test.iterrows():
            neigbors = find_neighbors(team, training, weights)
            tid = team['Team'] + str(team['Year'])
            ref[tid] = neigbors

    for k in range(K_range[0], K_range[1]):
        ks[k] = 0
        for _,team in test.iterrows():
            tid = team['Team'] + str(team['Year'])
            mean, std_dev = get_win_pred(team, k, ref=ref)
            if std_dev:
                off = abs(team['Wins']-mean)/std_dev
            else:
                off = abs(team['Wins']-mean)/.2
            ks[k] += off
        ks[k] /= size
    return ks


def find_best_weights_and_k(test, training, limit):
    # Establish dict tracking error of each weighting
    var_total_offs = {}
    for var in [item for item in important_stuff if item not in ["Region", "Year","Post-Season Tournament"]]:
        var_total_offs[var] = {}
        for i in range(0,weight_max+1):
            var_total_offs[var][i] = 0

    # Find error of many weight combos
    start = time.time()
    for weights in generate_configs(weight_max, limit):
        k_confs = find_best_k(training,test,k_range,weights)
        bestk = min(k_confs, key=k_confs.get)
        for var in [item for item in important_stuff if item not in ["Region","Year","Post-Season Tournament"]]:
            var_total_offs[var][weights[var]] += k_confs[bestk]

    # Find which weigts the data performed best at
    best_weights = {}
    for outer_key, inner_dict in var_total_offs.items():
        min_key = min(inner_dict, key=inner_dict.get)
        best_weights[outer_key] = min_key

    # Get best K for the best weight set
    k_confs = find_best_k(training,test,k_range,best_weights)
    bestk = min(k_confs, key=k_confs.get)
    return best_weights, bestk


def run_trials(data, trial_time_limit, split_size):    
    w_list = []
    k_list = []
    for i in range(trials):
        test = data.sample(n=split_size)
        training = data.drop(test.index)
        weights, k = find_best_weights_and_k(test, training, trial_time_limit)
        w_list.append(weights)
        k_list.append(k)

    best_k = round(sum(k_list)/len(k_list))
    sum_dict = {}
    for d in w_list:
        for key, value in d.items():
            if key in sum_dict:
                sum_dict[key] += value
            else:
                sum_dict[key] = value
    num_dicts = len(k_list)
    avg_ws = {key: sum_value / num_dicts for key, sum_value in sum_dict.items()}
    return best_k, avg_ws


def predict_new_data(new, train, k, ws):
    preds = []
    for _,team in new.iterrows():
        mean, std_dev = get_win_pred(team, k, training=train, weights=ws)
        preds.append((team['Team'], team['Seed'], team['Region'], round(mean, 4), round(std_dev,4)))
    
    return pd.DataFrame(preds, columns = ['Team', 'Seed', 'Region', 'Wins', 'Dev'])

def pick_winner(data, t1, t2, r):
    t1mean = data[data['Team'] == t1]['Wins'].values
    t1dev = data[data['Team'] == t1]['Dev'].values
    t2mean = data[data['Team'] == t2]['Wins'].values
    t2dev = data[data['Team'] == t2]['Dev'].values

    t1cdf = .5 * (1+math.erf((r-t1mean)/ (t1dev*math.sqrt(2))))
    t2cdf = .5 * (1+math.erf((r-t2mean)/ (t2dev*math.sqrt(2))))

    prob_t1 = 1-t1cdf
    prob_t2 = 1-t2cdf

    total = prob_t1 + prob_t2
    prob_t1 /= total
    prob_t2 /= total

    print("--------------")
    print(f"{t1}: {round(prob_t1, 5)}")
    print(f"{t2}: {round(prob_t2, 5)}")

    r = random.random()
    if r > prob_t1:
        print(t2)
        return t2
    else:
        print(t1)
        return t1

def predict_round(df, teams, round, max, cap):
    for i in range(1,max):
        t1 = teams[i]
        t2 = teams[cap-i]
        winner = pick_winner(df, t1, t2, round)
        if t1 != winner:
            teams[i] = t2
    print("--------------")
    return teams

def predict_region(region):
    csv_file_path = 'TeamPredictions.csv'
    df = pd.read_csv(csv_file_path)
    teams = {}
    for i in range(1,17):
        ts = df.loc[(df['Seed'] == i) & (df['Region'] == region), 'Team'].values
        if len(ts) > 1:
            teams[i] = pick_winner(df, ts[0], ts[-1], 0)
        else:
            teams[i] = ts[0]
    
    teams = predict_round(df, teams, 1, 9, 17)
    print("")
    teams = predict_round(df, teams, 2, 5, 9)
    print("")
    teams = predict_round(df, teams, 3, 3, 5)
    print("")
    teams = predict_round(df, teams, 4, 2, 3)
    print("")
    return teams[1]
# --------Callable funtions---------


def generate_team_predictions():
    start = time.time()
    training, real = loadData()  
    split_size = int(len(training)*training_split_size)

    k, ws = run_trials(training, max_time/trials, split_size)
    pred = predict_new_data(real, training, k, ws)      
    pred.to_csv("TeamPredictions.csv", index=False)
    print(time.time() - start)

def display_team_preds():
    csv_file_path = 'TeamPredictions.csv'
    df = pd.read_csv(csv_file_path)
    show(df)

def ask_winner(df, round, t1, t2):
    csv_file_path = 'TeamPredictions.csv'
    df = pd.read_csv(csv_file_path)
    round = int(input("round: "))
    t1 = input("Team 1: ")
    t2 = input("Team 2: ")
    pick_winner(df, t1, t2, round)


def predict_tourney():
    winners = {}
    regions = ["South","Midwest", "East", "West"]
    for region in regions:
        print(f"========={region}=========")
        winner = predict_region(region)
        winners[region] = winner
    
    print("===============Final Four================")
    csv_file_path = 'TeamPredictions.csv'
    df = pd.read_csv(csv_file_path)
    w1 = pick_winner(df, winners["West"], winners["South"], 5)
    w2 = pick_winner(df, winners["East"], winners["Midwest"], 5)
    pick_winner(df, w1, w2, 6)
    
