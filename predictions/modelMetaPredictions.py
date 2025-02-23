import os
import pandas as pd
import shutil
import sys
from joblib import load

NUMBER_RESULTS = 6
NUMBER_MODELS = 7

path_m = os.path.abspath(__file__).replace('\\', '/')
sslash_positions = [pos for pos, char in enumerate(path_m) if char == '/']
BASE_PATH = path_m[:sslash_positions[-1]]

def doMeta(country, league):
    WORK_PATH = BASE_PATH + "/Leagues/" + country + "/" + league + "/"
    if not os.path.exists(WORK_PATH):
        return 0

    PREDICTIONS_PATH = WORK_PATH + "Predictions"
    GAMES_PATH = WORK_PATH + "Games/human.csv"
    if not os.path.exists(GAMES_PATH):
        return 0
    gamesF = pd.read_csv(GAMES_PATH)
    for i in range(0, NUMBER_RESULTS):
        lines = []
        typePath = PREDICTIONS_PATH + "/" + str(i) + "/"
        for j in range(0, NUMBER_MODELS):
            ppp_path = typePath + str(j) + "/"
            predFile = ppp_path + "predictedAi.csv"
            predIndexFile = ppp_path + "predictedIndexes.csv"
            if not os.path.exists(predFile) or not os.path.exists(predIndexFile):
                return 0
            df = pd.read_csv(predFile)
            for k in range(0, len(df)):
                if j == 0:
                    lines.append([])
                maxi = 3
                if i > 0:
                    maxi = 2
                for kk in range(0, maxi):
                    lines[k].append(df.iloc[k][str(kk)])
        
        shutil.copy2(predIndexFile, typePath)
        
        newI = 0
        maxi = 21
        if i > 0:
            newI = 1
            maxi = 14
        model1 = load("meta" + str(newI) + ".joblib")
        cols = []
        for j in range(0, maxi):
            cols.append(str(j))
        X = pd.DataFrame(lines, columns=cols)
        predicted = model1.predict(X)
        prob = model1.predict_proba(X)

        with open(typePath + "predictedAi.csv", "w") as f:
            if i == 0:
                f.write("0,1,2,result\n")
            else:
                f.write("0,1,result\n")
            for k in range(0, len(prob)):
                for j in range(0, len(prob[k])):
                    f.write(f"{prob[k][j]:.2f}")
                    f.write(",")
                f.write(f"{predicted[k]}")
                f.write("\n")
        
        with open(typePath + "predictedHuman.txt", "w", encoding="utf-8") as f:
            idF = pd.read_csv(predIndexFile)
            for k in range(0, len(idF)):
                index = idF.iloc[k]["index"]
                f.write(f"{gamesF.iloc[index]['9']} vs {gamesF.iloc[index]['10']}\n")
                if len(prob[k]) > 2:
                    f.write(f"0 {prob[k][0]:.2%} ---------> 1 {prob[k][1]:.2%} ---------> 2 {prob[k][2]:.2%}  ---------> predict {predicted[k]}\n")
                else:
                    f.write(f"0 {prob[k][0]:.2%} ---------> 1 {prob[k][1]:.2%} ---------> predict {predicted[k]}\n")

def doMetas():
    cls = pd.read_csv("ALLCountryLeaguesSorted.csv")
    for clsI in range(0, len(cls)):
        """
        working on 11 ----- England -> Premier League
        working on 12 ----- Spain -> La Liga
        working on 13 ----- Germany -> Bundesliga
        working on 14 ----- Italy -> Serie A
        working on 15 ----- France -> Ligue 1
        """
        country = cls.iloc[clsI]['0'].encode('utf-8').decode('latin-1')
        league = cls.iloc[clsI]['1'].encode('utf-8').decode('latin-1')
        print(f"working on {clsI} ----- {country} -> {league}")
        doMeta(country, league)

doMetas()