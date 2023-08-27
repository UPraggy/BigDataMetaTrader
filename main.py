import os
import pandas as pd
import MetaTrader5 as mt5

from googleFinance import getEBIT_ROIC 
from getAtivosDF import geraDFAtivos

os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar

dataSet = []

listaAtivos = ['PETR4','ABEV3','AAPL34','M1TA34']

EBIT_ROICList = getEBIT_ROIC([
	{'ativo' : 'PETR4', 'linkAtivoGoogle' : 'PETR4:BVMF'},
	{'ativo' : 'ABEV3', 'linkAtivoGoogle' : 'ABEV3:BVMF'},
	{'ativo' : 'AAPL34', 'linkAtivoGoogle' : 'AAPL34:BVMF'},
	{'ativo' : 'M1TA34', 'linkAtivoGoogle' : 'M1TA34:BVMF'}
	])


for x in range(len(listaAtivos)):
	ativoTEMP = listaAtivos[x]
	dataFrameTMP = geraDFAtivos(ativoTEMP)
	dataFrameTMP['EBIT'] = EBIT_ROICList[ativoTEMP]['EBIT']
	dataFrameTMP['ROIC'] = EBIT_ROICList[ativoTEMP]['ROIC']
	dataSet.append(dataFrameTMP)

#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']
dataSet = pd.concat(dataSet)
print(dataSet[dataSet['ativo'] == 'PETR4'])

dataSet['ranking_ev_ebit'] = dataSet.groupby('ativo')['EBIT'].rank(ascending = False)
dataSet['ranking_roic'] = dataSet.groupby('ativo')['ROIC'].rank(ascending = False)
dataSet['ranking_final'] = dataSet['ranking_ev_ebit'] + dataSet['ranking_roic']
dataSet['ranking_final'] = dataSet.groupby('ativo')['ranking_final'].rank()




#IBOVESPA
dataIbov = geraDFAtivos('IBOV')
print(dataIbov['last'])



