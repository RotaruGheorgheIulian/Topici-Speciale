import os
import pandas as pd
import shutil
import sys

NUMBER_RESULTS = 6
NUMBER_MODELS = 7

path_m = os.path.abspath(__file__).replace('\\', '/')
sslash_positions = [pos for pos, char in enumerate(path_m) if char == '/']
BASE_PATH = path_m[:sslash_positions[-1]]

def doModel(country, league):
    WORK_PATH = BASE_PATH + "/Leagues/" + country + "/" + league + "/"
    if not os.path.exists(WORK_PATH):
        return 0

    PREDICTIONS_PATH = WORK_PATH + "PastPredictions"
    if not os.path.exists(PREDICTIONS_PATH):
        os.mkdir(PREDICTIONS_PATH)
    
    for i in range(0, NUMBER_RESULTS):
        pp_path = PREDICTIONS_PATH + "/" + str(i)
        if not os.path.exists(pp_path):
            os.mkdir(pp_path)
        for j in range(0, NUMBER_MODELS):
            ppp_path = pp_path + "/" + str(j)
            if not os.path.exists(ppp_path):
                os.mkdir(ppp_path)
            ppp_path += "/All"
            if not os.path.exists(ppp_path):
                os.mkdir(ppp_path)
            to_path = ppp_path
            newI = 0
            if i > 0:
                newI = 1
            from_path = "C:/Users/Iulian/Desktop/Python/FastResults/BasePastPredictionsAll/" + str(newI) + "/" + str(j) + "/All"
            all_files = os.listdir(from_path)
            files_only = [f for f in all_files if os.path.isfile(os.path.join(from_path, f))]

            for file in files_only:
                file_to_copy = from_path + "/" + file
                shutil.copy2(file_to_copy, to_path)
            file_to_run = to_path + "/runner.py"
            with open(file_to_run) as f:
                # Add the folder containing the script to sys.path
                script_dir = os.path.dirname(os.path.abspath(file_to_run))
                sys.path.insert(0, script_dir)  # Add directory to Python path temporarily

                try:
                    exec_globals = {
                        '__file__': os.path.abspath(file_to_run)
                    }
                    exec(f.read(), exec_globals)
                except SystemExit:
                    print("All updated...")
                finally:
                    # Clean up by removing the script directory from sys.path
                    if script_dir in sys.path:
                        sys.path.remove(script_dir)
                print("\n")

def doModels():
    cls = pd.read_csv("CountryLeaguesSorted.csv")
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
        doModel(country, league)

doModels()