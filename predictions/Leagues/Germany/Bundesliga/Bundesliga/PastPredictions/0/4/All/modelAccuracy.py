import os
import pandas as pd
import numpy as np
import importlib
import modelSetup
importlib.reload(modelSetup)

path_m = os.path.abspath(__file__).replace('\\', '/')
MODEL_INDEXES_FILE = path_m.replace("/modelAccuracy.py", "/predictedIndexes.csv")
MODEL_PREDICTED_AI_FILE = path_m.replace("/modelAccuracy.py", "/predictedAi.csv")
MODEL_ACCURACY_FILE = path_m.replace("/modelAccuracy.py", "/accuracy.txt")

def printStats(what, freq):
    with open(MODEL_ACCURACY_FILE, "a", encoding="utf-8") as f:
        f.write(f"For {what}\n")
        good = np.trace(freq)
        nr = np.sum(freq)
        if nr > 0:
            f.write(f"Good: {good}/{nr} Percentage: {good/nr:.2%}\n")

        for a in range(0, modelSetup.setPredictors()):
            good = freq[a][a]
            nr = 0
            for b in range(0, modelSetup.setPredictors()):
                nr += freq[a][b]
            if nr > 0:
                f.write(f"Predicted {a} good: {good}/{nr} Percentage: {good/nr:.2%}\n")


def calculateAccuracy():
    path_here = os.path.abspath(__file__).replace('\\', '/')
    ACTUAL_COLUMN = "result" + path_here.split('/')[10]
    sslash_positions = [pos for pos, char in enumerate(path_here) if char == '/']
    PATH = path_here[:sslash_positions[-5]] + "/Games/"
    pda = pd.read_csv(PATH + "ai.csv")
    if not os.path.exists(MODEL_PREDICTED_AI_FILE):
        exit(0)
    pdb = pd.read_csv(MODEL_PREDICTED_AI_FILE)
    pdc = pd.read_csv(MODEL_INDEXES_FILE)

    with open(MODEL_ACCURACY_FILE, "w", encoding="utf-8") as f:
        f.write('')

    fr = np.zeros((modelSetup.setPredictors(), modelSetup.setPredictors()), dtype=int)
    frs = np.zeros((modelSetup.setPredictors(), modelSetup.setPredictors()), dtype=int)
    lastSeason = 1

    for i in range(0, len(pdc)):
        index = pdc.iloc[i]["index"]
        predictedResult = pdb.iloc[i]["result"].astype(int)
        actualResult = pda.iloc[index][ACTUAL_COLUMN].astype(int)
        fr[predictedResult][actualResult] += 1

        currSeason = pda.iloc[index]["season"].astype(int)
        if currSeason == lastSeason:
            frs[predictedResult][actualResult] += 1
        else:
            printStats("Season " + str(lastSeason), frs)
            lastSeason = currSeason
            frs = np.zeros((modelSetup.setPredictors(), modelSetup.setPredictors()), dtype=int)
            frs[predictedResult][actualResult] += 1
    
    printStats("Season " + str(lastSeason), frs)
    printStats("Total", fr)

calculateAccuracy()