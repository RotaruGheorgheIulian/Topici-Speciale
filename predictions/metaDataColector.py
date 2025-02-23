import os
import pandas as pd
import shutil
import sys

NUMBER_RESULTS = 6
NUMBER_MODELS = 7

path_m = os.path.abspath(__file__).replace('\\', '/')
sslash_positions = [pos for pos, char in enumerate(path_m) if char == '/']
BASE_PATH = path_m[:sslash_positions[-1]]

def doColector(country, league):
    WORK_PATH = BASE_PATH + "/Leagues/" + country + "/" + league + "/"
    if not os.path.exists(WORK_PATH):
        return 0

    PREDICTIONS_PATH = WORK_PATH + "PastPredictions"
    GAMES_PATH = WORK_PATH + "Games/ai.csv"
    if not os.path.exists(GAMES_PATH):
        return 0
    gamesF = pd.read_csv(GAMES_PATH)
    for i in range(0, NUMBER_RESULTS):
        lines = []
        for j in range(0, NUMBER_MODELS):
            ppp_path = PREDICTIONS_PATH + "/" + str(i) + "/" + str(j) + "/All/"
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
        idF = pd.read_csv(predIndexFile)
        for k in range(0, len(idF)):
            index = idF.iloc[k]["index"]
            lines[k].append(gamesF.iloc[index]["result" + str(i)].astype(int))
        
        newI = 0
        if i > 0:
            newI = 1
        with open("metadata/" + str(newI) + ".csv", "a") as f:
            for line in lines:
                for j in range(0, len(line)):
                    f.write(f"{line[j]:.2f}")
                    if j < len(line) - 1:
                        f.write(",")
                f.write("\n")

def doColectors():
    with open("metadata/0.csv", "w") as f:
            for j in range(0, 21):
                f.write(str(j))
                f.write(",")
            f.write("result\n")
    with open("metadata/1.csv", "w") as f:
            for j in range(0, 14):
                f.write(str(j))
                f.write(",")
            f.write("result\n")
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
        doColector(country, league)

doColectors()