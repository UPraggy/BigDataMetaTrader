import numpy as np
import pandas as pd
from datetime import datetime

def getPrevisaoModel(dataSet, scalerT1, modelT1, dias):
	# @title Prev
	testeDATA = dataSet.copy()

	#um dia antes
	TMPtesteDATA = testeDATA.loc[(testeDATA.index.day == dias[-2:-1][0])].copy()
	cotacao_teste = TMPtesteDATA['last'].to_numpy().reshape(-1, 1);


	#transforma em 0 e 1 para avaliação
	cotacao_teste_scaled = scalerT1.transform(cotacao_teste)

	teste_x = []
	for i in range(60, len(cotacao_teste_scaled)):
	    teste_x.append(cotacao_teste_scaled[i-60:i, 0])

	teste_x = np.array(teste_x)
	teste_x = np.reshape(teste_x, (teste_x.shape[0], teste_x.shape[1], 1))

	predictionsT2 = modelT1.predict(teste_x)

	#converte 0 e 1 nos dados originais
	predictionsT2 = scalerT1.inverse_transform(predictionsT2)

	teste_x = []
	for i in range(0, len(cotacao_teste_scaled)):
	    teste_x.append(cotacao_teste_scaled[i])

	teste_x = np.array(teste_x)
	teste_x = np.reshape(teste_x, (teste_x.shape[0], teste_x.shape[1], 1))

	predictionsT2 = modelT1.predict(teste_x)

	#converte 0 e 1 nos dados originais
	predictionsT2 = scalerT1.inverse_transform(predictionsT2)





	predictionsT2 = predictionsT2.flatten()

	# @title Ajustando diferença e mostrando preço real
	diferencaPrevEReal = TMPtesteDATA.filter(['last']).values.flatten().mean() - predictionsT2.mean()

	NovaPrevT3 = []

	for x in predictionsT2:
	  NovaPrevT3.append(x + diferencaPrevEReal)

	return NovaPrevT3