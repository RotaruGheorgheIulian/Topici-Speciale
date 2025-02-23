import os
import sys
import numpy as np
import pandas as pd
from joblib import dump
from joblib import load
import importlib
import modelSetup
importlib.reload(modelSetup)

path_m = os.path.abspath(__file__).replace('\\', '/')
MODEL_SAMPLE_FILE = path_m.replace("/model.py", "/modelSample.txt")
MODEL_FILE = path_m.replace("/model.py", "/model.joblib")
MODEL_INDEXES_FILE = path_m.replace("/model.py", "/predictedIndexes.csv")
MODEL_PREDICTED_AI_FILE = path_m.replace("/model.py", "/predictedAi.csv")

RESULT_COLUMN = "result" + path_m.split('/')[10]
sslash_positions = [pos for pos, char in enumerate(path_m) if char == '/']
GAMES_PATH = path_m[:sslash_positions[-5]] + "/Games/"
X = []
Y = []

df = pd.read_csv(GAMES_PATH + "ai.csv")
gdf = pd.read_csv(GAMES_PATH + "human.csv")

toExclude = ["id"]
COLUMNS_TO_KEEP = []
for x in df.columns:
    if x not in toExclude and not x.startswith("result"):
        COLUMNS_TO_KEEP.append(x)

seasons = []
seasonStart = []
for i in range(0, len(df)):
    if gdf.iloc[i]['4'] == "Match Finished":
        END = i + 1
    currSeason = gdf.iloc[i]['7'].astype(int)
    if len(seasons) == 0:
        seasons.append(currSeason)
        seasonStart.append(i + 1)
    if currSeason != seasons[-1]:
        seasons.append(currSeason)
        seasonStart.append(i + 1)
    else:
        seasonStart[-1] = i + 1
START = 50
if len(seasonStart) >= 4:
    START = seasonStart[-4]
if START < 50:
    exit(0)

def getLineForX(index):
    line = []
    for col in COLUMNS_TO_KEEP:
        line.append(df.iloc[index][col])
    return line

def loadModel():
    global X
    global Y
    global X_index
    global START
    global END
    if os.path.exists(MODEL_SAMPLE_FILE):
        with open(MODEL_SAMPLE_FILE, 'r') as file:
            START = int(file.readline().strip())
    
    if START >= END:
        sys.exit()

    for i in range(START - 50, START):
        X.append(getLineForX(i))
        Y.append(df.iloc[i][RESULT_COLUMN].astype(int))
    
    if os.path.exists(MODEL_FILE):
        return load(MODEL_FILE)
    
    with open(MODEL_INDEXES_FILE, "w", encoding="utf-8") as f:
        f.write("index\n")

    with open(MODEL_PREDICTED_AI_FILE, "w", encoding="utf-8") as f:
        f.write("0,1,2,result\n")

    model = modelSetup.setModel()
    model.fit(X, Y)
    dump(model, MODEL_FILE)
    with open(MODEL_SAMPLE_FILE, 'w') as f:
        f.write(f"{START}\n")
    return model

def doModel():
    global X
    global Y
    global X_index
    global START
    global END
    model = loadModel()

    X_pred = []
    Y_pred = []
    X_index = []
    if START < END:
        lastRound = df.iloc[START]["round"]

    for i in range(START, END):
        currentRound = df.iloc[i]["round"]

        if currentRound == lastRound:
            X_pred.append(getLineForX(i))
            Y_pred.append(df.iloc[i][RESULT_COLUMN].astype(int))
            X_index.append(i)
        else:
            predicted = model.predict(X_pred)
            probabilities = model.predict_proba(X_pred)

            X += X_pred
            Y += Y_pred
            model.fit(X, Y)
            dump(model, MODEL_FILE)
            with open(MODEL_SAMPLE_FILE, 'w') as f:
                f.write(f"{i}\n")

            with open(MODEL_INDEXES_FILE, "a", encoding="utf-8") as f:
                for j in range(0, len(X_index)):
                    f.write(f"{X_index[j]}\n")

            with open(MODEL_PREDICTED_AI_FILE, "a", encoding="utf-8") as f:
                for j in range(0, len(X_index)):
                    f.write(f"{probabilities[j][0]:.2f},{probabilities[j][1]:.2f},{probabilities[j][2]:.2f},{predicted[j]}\n")

            lastRound = currentRound
            X_pred = [getLineForX(i)]
            Y_pred = [df.iloc[i][RESULT_COLUMN].astype(int)]
            X_index = [i]
    
    if len(Y_pred) > 0:
        predicted = model.predict(X_pred)
        probabilities = model.predict_proba(X_pred)

        X += X_pred
        Y += Y_pred
        model.fit(X, Y)
        dump(model, MODEL_FILE)
        with open(MODEL_SAMPLE_FILE, 'w') as f:
            f.write(f"{END}\n")

        with open(MODEL_INDEXES_FILE, "a", encoding="utf-8") as f:
            for j in range(0, len(X_index)):
                f.write(f"{X_index[j]}\n")

        with open(MODEL_PREDICTED_AI_FILE, "a", encoding="utf-8") as f:
            for j in range(0, len(X_index)):
                f.write(f"{probabilities[j][0]:.2f},{probabilities[j][1]:.2f},{probabilities[j][2]:.2f},{predicted[j]}\n")

doModel()