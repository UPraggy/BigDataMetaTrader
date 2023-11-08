import os
import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5
from googleFinance import getEBIT_ROIC 

def getCarteira(mt5, listaAtivos = ''):
	dataSet = []

	# Cria um array pegando todos os ativos do MetaTrader, filtra os que são do IBOVESPA(B3) e filtra os ativos compraveis que terminam com 3 ou 4

	if (listaAtivos == ''):
		listaAtivos = ['PETR4','ABEV3','AAPL34','M1TA34','TEND3','PLPL3','PINE4']
	else:
		listaAtivos = [x.name for x in mt5.symbols_get() if "BOVESPA\\A VISTA" in x.path and x.name.endswith(('4')) and len(x.name) <= 6]

	ativos = [{'ativo' : nome, 'linkAtivoGoogle' : nome+':BVMF'} for nome in listaAtivos]

	EBIT_ROICList = getEBIT_ROIC(ativos)

	dataFrameTMP = pd.DataFrame(columns=['ativo', 'EBIT', 'ROIC'])


	#CRIANDO DATAFRAME COM TODOS ATIVOS
	for x in EBIT_ROICList.keys():
		dataFrameTMP.loc[len(dataFrameTMP)] = {
												'ativo':x,
		                    'EBIT':EBIT_ROICList[x]['EBIT'],
		                    'ROIC' : EBIT_ROICList[x]['ROIC'],
												}

	#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']

	#RANKEANDO EBIT
	dataFrameTMP['ranking_ev_ebit'] = dataFrameTMP['EBIT'].rank(ascending = False)

	#RANKEANDO ROIC
	dataFrameTMP['ranking_roic'] = dataFrameTMP['ROIC'].rank(ascending = False)

	#RANKEANDO DE ACORDO COM RANKINGS ANTERIORES
	dataFrameTMP['ranking_final'] = dataFrameTMP['ranking_ev_ebit'] + dataFrameTMP['ranking_roic']
	dataFrameTMP['ranking_final'] = dataFrameTMP['ranking_final'].rank()

	# DELETANDO COLUNAS NÃO MAIS NECESSÁRIAS
	del dataFrameTMP['ranking_ev_ebit']
	del dataFrameTMP['ranking_roic']

	print("##### RANKING FINAL DE ATIVOS #####")
	topAtivos = dataFrameTMP.sort_values(['ranking_final','ROIC','EBIT'])
	print(topAtivos)


	print("\n\n##### MELHOR ATIVO DO DIA #####\n")
	print(topAtivos.iloc[0]['ativo'])
	
	return topAtivos.iloc[0]['ativo']


