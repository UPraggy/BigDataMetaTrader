import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

def geraTrain(dataframe):
    # Use todos os dados para o MinMaxScaler
    data = dataframe['last'].tail(500).values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_normalized = scaler.fit_transform(data)
    
    x_train = []
    y_train = []

    for i in range(60, len(data_normalized)):
      x_train.append(data_normalized[i-60:i, 0])
      y_train.append(data_normalized[i, 0])

    #convertendo treinos para numpy
    x_train, y_train = np.array(x_train), np.array(y_train)
  
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return [x_train, y_train, scaler]

def atualizaPrev(novoDataframe, xTreinoAntigo, YTreinoAntigo, epochs=1, batch_size=32):

    [x_trainT1, y_trainT1, scalerT1] = geraTrain(novoDataframe)
    pretrained_model = load_model('modeloT1.keras')
    model = Sequential()
    for layer in pretrained_model.layers:
        model.add(layer)
    model.add(Dense(1))  
    weighting_factor = 0.1
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.0001))

    num_old_samples = len(x_trainT1)
    weights = np.ones((len(x_trainT1), 1))
    weights[:num_old_samples] *= weighting_factor
    model.fit(x_trainT1, y_trainT1, sample_weight=weights, epochs=epochs, batch_size=batch_size, verbose='2')
    return [x_trainT1, y_trainT1, scalerT1, model]
