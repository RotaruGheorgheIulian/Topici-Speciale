from sklearn.neighbors import KNeighborsClassifier

def setModel():
    return KNeighborsClassifier(n_neighbors=13)

def setPredictors():
    return 2