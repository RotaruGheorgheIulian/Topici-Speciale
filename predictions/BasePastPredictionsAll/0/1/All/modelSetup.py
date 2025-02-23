from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def setModel():
    N_ESTIMATORS = 1000
    RANDOM_STATE = 42
    return make_pipeline(StandardScaler(), LogisticRegression(solver='lbfgs', max_iter=N_ESTIMATORS, random_state=RANDOM_STATE, class_weight='balanced'))

def setPredictors():
    return 3