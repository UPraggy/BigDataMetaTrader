from tensorflow.python import training
# @title LSTM
import pandas as pd;
from sklearn.preprocessing import MinMaxScaler;
from keras.models import Sequential;
from keras.layers import Dense, LSTM;
import matplotlib.pyplot as plt;
from datetime import datetime;
from datetime import timedelta;
import math
import numpy as np
def LSTMFunc(dataSet, dias): 

	pd.options.mode.chained_assignment = None;

	testeDATAT1 = dataSet.copy()

	TMPtesteDATAT1 = testeDATAT1.loc[(testeDATAT1.index.day <= dias)].copy()
	cotacaoT1 = TMPtesteDATAT1.filter(['last']).values;
	training_data_lenT1 = len(cotacaoT1)


	scalerT1 = MinMaxScaler(feature_range=(0,1))
	scaled_dataT1 = scalerT1.fit_transform(cotacaoT1)
	train_dataT1 = scaled_dataT1[0: training_data_lenT1, :]

	x_trainT1 = []
	y_trainT1 = []

	for i in range(60, len(train_dataT1)):
	  x_trainT1.append(train_dataT1[i-60:i, 0])
	  y_trainT1.append(train_dataT1[i, 0])
	  # if i<= 60:
	  #   print(x_trainT1)
	  #   print(y_trainT1)


	#convertendo treinos para numpy
	x_trainT1, y_trainT1 = np.array(x_trainT1), np.array(y_trainT1)


	#Reshape os dados
	x_trainT1 = np.reshape(x_trainT1, (x_trainT1.shape[0], x_trainT1.shape[1], 1))



	#construindo modelo LSTM

	modelT1 = Sequential()
	modelT1.add(LSTM(50, return_sequences=True, input_shape = (x_trainT1.shape[1], 1)));
	modelT1.add(LSTM(50, return_sequences=False));
	modelT1.add(Dense(25));
	modelT1.add(Dense(1));



	#compilando o modelo
	modelT1.compile(optimizer="adam", loss="mean_squared_error");

	#treinando modelo 15 15
	modelT1.fit(x_trainT1, y_trainT1, batch_size=50, epochs=1);

	# Salve o modelo inteiro (arquitetura + pesos)
	modelT1.save('modeloT1.keras')


	return [x_trainT1, y_trainT1, modelT1,scalerT1]