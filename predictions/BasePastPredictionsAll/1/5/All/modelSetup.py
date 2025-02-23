from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def setModel():
    RANDOM_STATE = 42
    return make_pipeline(StandardScaler(), SVC(kernel='linear', probability=True, random_state=RANDOM_STATE))

def setPredictors():
    return 2