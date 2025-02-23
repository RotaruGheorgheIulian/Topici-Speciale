from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from keras import layers

def create_ann(input_dim, num_classes):
    """Creates a four-layer Artificial Neural Network (ANN)."""
    model = layers.Sequential([
        layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def setModel(resOuts, nr):
    MAX_DEPTH = 6
    N_ESTIMATORS = 1000
    RANDOM_STATE = 42
    NUM_CLASS = setPredictors(resOuts)
    
    if nr == 0:
        return make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH, random_state=RANDOM_STATE, class_weight='balanced'))
    if nr == 1:
        return make_pipeline(StandardScaler(), LogisticRegression(solver='lbfgs', max_iter=N_ESTIMATORS, random_state=RANDOM_STATE, class_weight='balanced'))
    if nr == 2:
        return GaussianNB()
    if nr == 3:
        return ExtraTreesClassifier(n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH, random_state=RANDOM_STATE, class_weight='balanced')
    if nr == 4:
        return KNeighborsClassifier(n_neighbors=13)
    if nr == 5:
        return make_pipeline(StandardScaler(), SVC(kernel='linear', probability=True, random_state=RANDOM_STATE))
    if nr == 6:
        return create_ann(341, NUM_CLASS)

def setPredictors(resOuts):
    if resOuts == 0:
        return 2
    return 3
