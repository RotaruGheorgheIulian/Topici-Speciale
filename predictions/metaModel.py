import pandas as pd
from modelSetup import setModel
from joblib import dump
PROB = 0.7

def doMeta(nnr, modelNr):
    file_path = "metadata/" + str(nnr) + ".csv"
    data = pd.read_csv(file_path)
    X = data.iloc[:, :-1]
    Y = data.iloc[:, -1].astype(int)
    model = setModel(1 - nnr, modelNr)
    model.fit(X, Y)
    dump(model, "meta" + str(nnr) + ".joblib")

    predicted = model.predict(X)
    prob = model.predict_proba(X)

    good = 0
    nr = 0
    for i in range(0, len(Y)):
        if prob[i][predicted[i]] < PROB:
            continue
        if predicted[i] == Y[i]:
            good += 1
        nr += 1
    print(f"{good} / {nr} percent: {good/nr:.2f}")

for modo in range(0, 2):
    doMeta(modo, 0)