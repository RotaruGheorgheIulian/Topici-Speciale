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

def setModel():
    NUM_CLASS = setPredictors()
    return create_ann(346, NUM_CLASS)

def setPredictors():
    return 3