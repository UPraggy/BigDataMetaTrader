from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

def limitaPeriodo(horas, ticks, limitPeriodo):
	if limitPeriodo:
		return ticks
	else:
	 	return horas * 10000

def geraDFAtivos(ativoSelecionado, horasDif = 10, seconds = 0, minutes=0,
	dias = 0, ticks=1, limitPeriodo = False):


	while True:
		#tentar pegar a ultima data do ativo
		date = datetime.now() - timedelta(hours=horasDif, days=dias, minutes=minutes, seconds=seconds)


		flags = mt5.COPY_TICKS_ALL #Pegando todas as variações no preço 

		dataSet = mt5.copy_ticks_from(ativoSelecionado, 
					date,limitaPeriodo(horasDif, ticks, limitPeriodo), flags)#10000

		dataSetDF = pd.DataFrame(dataSet)

		if (dataSetDF.empty):
			dias += 1
			pass #dataframe vazio
		else:
			break;

	dataSetDF['time'] = pd.to_datetime(dataSetDF['time'], unit='s')
	dataSetDF['ativo'] = ativoSelecionado
	return dataSetDF