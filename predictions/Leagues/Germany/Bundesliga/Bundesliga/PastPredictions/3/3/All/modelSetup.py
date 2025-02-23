from sklearn.ensemble import ExtraTreesClassifier

def setModel():
    MAX_DEPTH = 6
    N_ESTIMATORS = 1000
    RANDOM_STATE = 42
    return ExtraTreesClassifier(n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH, random_state=RANDOM_STATE, class_weight='balanced')

def setPredictors():
    return 2