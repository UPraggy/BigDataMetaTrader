import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

def geraTrain(dataframe):
    last_row = dataframe['last'].iloc[-1]
    last_row_reshaped = np.reshape(last_row, (1, -1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    last_row_normalized = scaler.fit_transform(last_row_reshaped)
    x_train = last_row_normalized[:-1]
    y_train = last_row_normalized[-1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    return [x_train, y_train, scaler]

def atualizaPrev(novoDataframe, xTreinoAntigo, YTreinoAntigo, epochs=10, batch_size=32):
    [x_trainT1, y_trainT1, scalerT1] = geraTrain(novoDataframe)
    pretrained_model = load_model('modeloT1.keras')
    model = Sequential()
    for layer in pretrained_model.layers:
        model.add(layer)
    model.add(Dense(1))  
    weighting_factor = 0.1
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.0001))
    X_combined = np.vstack((xTreinoAntigo, x_trainT1))
    y_combined = np.vstack((YTreinoAntigo, y_trainT1))
    num_old_samples = len(xTreinoAntigo)
    weights = np.ones((len(X_combined), 1))
    weights[:num_old_samples] *= weighting_factor
    model.fit(X_combined, y_combined, sample_weight=weights, epochs=epochs, batch_size=batch_size, verbose='2')
    return [X_combined, y_combined, scalerT1, model]
