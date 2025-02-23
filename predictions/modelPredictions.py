import os
import pandas as pd
from joblib import dump
from joblib import load
from modelSetup import setModel

NUMBER_RESULTS = 6
NUMBER_MODELS = 7

X = []
Y = [[] for _ in range(NUMBER_RESULTS)]
COLUMNS_TO_KEEP = []
START = 50

path_m = os.path.abspath(__file__).replace('\\', '/')
sslash_positions = [pos for pos, char in enumerate(path_m) if char == '/']
BASE_PATH = path_m[:sslash_positions[-1]]

def getLineForX(index):
    global df
    line = []
    for col in COLUMNS_TO_KEEP:
        line.append(df.iloc[index][col])
    return line

def getModel():
    global df
    global START
    global PREDICTIONS_PATH

    model = [[0 for _ in range(NUMBER_MODELS)] for __ in range(NUMBER_RESULTS)]

    loaded_models = 0
    for r in range(0, NUMBER_RESULTS):
        for j in range(0, NUMBER_MODELS):
            PREFIX_PATH = PREDICTIONS_PATH + "/" + str(r) + "/" + str(j)
            if os.path.exists(PREFIX_PATH + "/modelSample.txt") and os.path.exists(PREFIX_PATH + "/model.joblib"):
                with open(PREFIX_PATH + "/modelSample.txt", 'r') as file:
                    sampleSize = int(file.readline().strip())
                if sampleSize == START - 1:
                    loaded_models += 1
                    model[r][j] = load(PREFIX_PATH + "/model.joblib")
    if loaded_models == NUMBER_MODELS * NUMBER_RESULTS:
        return model
    X = []
    Y = [[] for _ in range(NUMBER_RESULTS)]
    maximStart = 0
    for i in range(0, START):
        X.append(getLineForX(i))
        for j in range(0, NUMBER_RESULTS):
            Y[j].append(df.iloc[i]["result" + str(j)].astype(int))
    
    for r in range(0, NUMBER_RESULTS):
        for j in range(0, NUMBER_MODELS):
            if not model[r][j]:
                print(f"Working on result {r} model {j}")
                model[r][j] = setModel(r, j)
                model[r][j].fit(X, Y[r])
                PREFIX_PATH = PREDICTIONS_PATH + "/" + str(r) + "/" + str(j)
                dump(model[r][j], PREFIX_PATH + "/model.joblib")
                with open(PREFIX_PATH + "/modelSample.txt", 'w') as f:
                    f.write(f"{START - 1}\n")
    return model

def doModel(country, league):
    global df
    global START
    global WORK_PATH
    global COLUMNS_TO_KEEP
    global PREDICTIONS_PATH

    model = [[[] for _ in range(NUMBER_MODELS)] for __ in range(NUMBER_RESULTS)]
    COLUMNS_TO_KEEP = []

    WORK_PATH = BASE_PATH + "/Leagues/" + country + "/" + league + "/"
    if not os.path.exists(WORK_PATH):
        return 0
    GAMES_PATH = WORK_PATH + "Games/"

    PREDICTIONS_PATH = WORK_PATH + "Predictions"
    if not os.path.exists(PREDICTIONS_PATH):
        os.mkdir(PREDICTIONS_PATH)
    for r in range(0, NUMBER_RESULTS):
        predRes = PREDICTIONS_PATH + "/" + str(r)
        if not os.path.exists(predRes):
            os.mkdir(predRes)
        for j in range(0, NUMBER_MODELS):
            predModel = predRes + "/" + str(j)
            if not os.path.exists(predModel):
                os.mkdir(predModel)

    df = pd.read_csv(GAMES_PATH + "ai.csv")
    gdf = pd.read_csv(GAMES_PATH + "human.csv")

    toExclude = ["id"]
    COLUMNS_TO_KEEP = []
    for x in df.columns:
        if x not in toExclude and not x.startswith("result"):
            COLUMNS_TO_KEEP.append(x)

    END = len(df)
    for i in range(0, END):
        if gdf.iloc[i]['4'] == "Match Finished":
            START = i + 1
    
    if START >= END:
        return 0
    model = getModel()
    X_pred = []
    X_index = []
    uniqueTeams = []

    for i in range(START, END):
        if df.iloc[i]["homeTeam"].astype(int) not in uniqueTeams and df.iloc[i]["awayTeam"].astype(int) not in uniqueTeams:
            X_new = getLineForX(i)
            X_pred.append(X_new)
            X_index.append(i)
            uniqueTeams.append(df.iloc[i]["homeTeam"].astype(int))
            uniqueTeams.append(df.iloc[i]["awayTeam"].astype(int))
    
    for r in range(0, NUMBER_RESULTS):
        for j in range(0, NUMBER_MODELS):
            PREFIX_PATH = PREDICTIONS_PATH + "/" + str(r) + "/" + str(j)
            predicted = model[r][j].predict(X_pred)
            probabilities = model[r][j].predict_proba(X_pred)
            with open(PREFIX_PATH + "/predictedIndexes.csv", "w", encoding="utf-8") as f:
                f.write("index\n")
                for i in range(0, len(X_index)):
                    f.write(f"{X_index[i]}\n")

            with open(PREFIX_PATH + "/predictedAi.csv", "w", encoding="utf-8") as f:
                f.write("0,1,2,result\n")
                for i in range(0, len(X_index)):
                    if len(probabilities[i]) > 2:
                        f.write(f"{probabilities[i][0]:.2f},{probabilities[i][1]:.2f},{probabilities[i][2]:.2f},{predicted[i]}\n")
                    else:
                        f.write(f"{probabilities[i][0]:.2f},{probabilities[i][1]:.2f},0,{predicted[i]}\n")

            with open(PREFIX_PATH + "/predictedHuman.txt", "w", encoding="utf-8") as f:
                for i in range(0, len(X_index)):
                    index = X_index[i]
                    f.write(f"{gdf.iloc[index]['9']} vs {gdf.iloc[index]['10']}\n")
                    if len(probabilities[i]) > 2:
                        f.write(f"0 {probabilities[i][0]:.2%} ---------> 1 {probabilities[i][1]:.2%} ---------> 2 {probabilities[i][2]:.2%}  ---------> predict {predicted[i]}\n")
                    else:
                        f.write(f"0 {probabilities[i][0]:.2%} ---------> 1 {probabilities[i][1]:.2%} ---------> predict {predicted[i]}\n")
def doModels():
    cls = pd.read_csv("ALLCountryLeaguesSorted.csv")
    for clsI in range(0, len(cls)):
        country = cls.iloc[clsI]['0'].encode('utf-8').decode('latin-1')
        league = cls.iloc[clsI]['1'].encode('utf-8').decode('latin-1')
        print(f"working on {clsI} ----- {country} -> {league}")
        doModel(country, league)

doModels()