import os
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import matplotlib.pyplot as plt


from getAtivosDF import geraDFAtivos
from configuraCompra import configuraBaseCompra

os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar

dataSet = []

listaAtivos = ['PETR4','ABEV3','AAPL34','M1TA34']

dataSet = geraDFAtivos('PETR4', horasDif = 10, ticks=1000, 
	limitPeriodo=True)
futureDataSet = geraDFAtivos('PETR4', horasDif = 9, minutes = 32, ticks=1, 
	limitPeriodo=True)

#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']
print(dataSet)
print(futureDataSet)
pd.concat([dataSet,futureDataSet], ignore_index=True)


dataSet = configuraBaseCompra(dataSet,'PETR4')

