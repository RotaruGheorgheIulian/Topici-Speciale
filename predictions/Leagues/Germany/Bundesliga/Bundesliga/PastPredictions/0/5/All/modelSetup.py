from xgboost import XGBClassifier

def setModel():
    MAX_DEPTH = 6
    N_ESTIMATORS = 1000
    RANDOM_STATE = 42
    return XGBClassifier(n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH, objective='multi:softmax', num_class=setPredictors(), random_state=RANDOM_STATE)

def setPredictors():
    return 3