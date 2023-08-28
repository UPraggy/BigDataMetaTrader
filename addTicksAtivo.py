from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd

def geraDFAtivos(ativoSelecionado):

	# Subtrai duas horas da data e hora atual
	date = datetime.now() - timedelta(seconds=2, hours=6)


	flags = mt5.COPY_TICKS_ALL #Pegando todas as variações no preço 

	dataSet = mt5.copy_ticks_from(ativoSelecionado, 
				date, 10, flags)

	dataSetDF = pd.DataFrame(dataSet)

	dataSetDF['time'] = pd.to_datetime(dataSetDF['time'], unit='s')
	dataSetDF['ativo'] = ativoSelecionado
	return dataSetDF