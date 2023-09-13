import os
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import matplotlib.pyplot as plt
import time

from getAtivosDF import geraDFAtivos
from configuraCompra import configuraBaseCompra, trataDF, configuraBaseUltimoIndice

os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar

dataSet = []

#Bolsa Offline/fechada
dataSet = geraDFAtivos('PETR4')
#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']

dataSet = trataDF(dataSet,'PETR4')

#criando simulacao de um dataframe com os tempos futuros
futureDataSet = dataSet.iloc[100:].copy()

#criando simulacao de um dataframe com os tempos atuais
dataSet = dataSet.iloc[:100].copy()
dataSet = configuraBaseCompra(dataSet)

#Retirando uma linha (como se o tempo estivesse correndo)

tempoFuturo = 1
while True:
	# transpose convertendo para que dê para juntar no dataframe atual 
	tmp = futureDataSet.iloc[tempoFuturo].to_frame().transpose()

	#adicionando linha do futuro
	dataSet = pd.concat([dataSet,tmp])

	#configurando compra ou não
	dataSet = configuraBaseUltimoIndice(dataSet)
	os.system('cls' if os.name == 'nt' else 'clear')
	print(dataSet)
	time.sleep(2)
	tempoFuturo += 1 
