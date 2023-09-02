from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

def geraDFAtivos(ativoSelecionado, horasDif = 10):

	#tentar pegar a ultima data do ativo
	dias = 0

	while True:
		# Subtrai duas horas da data e hora atual
		date = datetime.now() - timedelta(hours=horasDif, days=dias)


		flags = mt5.COPY_TICKS_ALL #Pegando todas as variações no preço 

		dataSet = mt5.copy_ticks_from(ativoSelecionado, 
					date, horasDif*10000, flags)

		dataSetDF = pd.DataFrame(dataSet)

		if (dataSetDF.empty):
			dias += 1
			pass #dataframe vazio
		else:
			break;

	dataSetDF['time'] = pd.to_datetime(dataSetDF['time'], unit='s')
	dataSetDF['ativo'] = ativoSelecionado
	return dataSetDF