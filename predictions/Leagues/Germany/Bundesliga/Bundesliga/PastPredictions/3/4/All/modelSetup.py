from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def setModel():
    N_ESTIMATORS = 1000
    RANDOM_STATE = 42
    return make_pipeline(StandardScaler(), MLPClassifier(solver='sgd', learning_rate='adaptive', hidden_layer_sizes=(400, 200, 50), early_stopping=True, max_iter=N_ESTIMATORS, random_state=RANDOM_STATE))

def setPredictors():
    return 3