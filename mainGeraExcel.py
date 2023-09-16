import os
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import matplotlib.pyplot as plt
# from googleFinance import getEBIT_ROIC 
from getAtivosDF import geraDFAtivos
from configuraCompra import configuraBaseCompra, trataDF, configuraBaseUltimoIndice

os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar

dataSet = []

listaAtivos = ['PETR4','ABEV3','AAPL34','M1TA34']


for x in range(len(listaAtivos)):
	ativoTEMP = listaAtivos[x]
	dataFrameTMP = geraDFAtivos(ativoTEMP)
	dataSet.append(dataFrameTMP)

#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']
dataSet = pd.concat(dataSet)

#Bolsa Offline/fechada
dataSet = geraDFAtivos('PETR4',horasDif=5*24)
#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']

dataSet = trataDF(dataSet,'PETR4')
print(dataSet)
dataSet.to_excel('MetaTrader5dias.xlsx', index=False)
