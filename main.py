import os
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
import matplotlib.pyplot as plt
# from googleFinance import getEBIT_ROIC 
from getAtivosDF import geraDFAtivos
from configuraCompra import configuraBaseCompra

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


dataSet = configuraBaseCompra(dataSet,'PETR4')



# GERANDO GRAFICO e "Comprando"
data_compra = []
data_venda = []

for i in range(len(dataSet)):

    if "sim" in dataSet['compra'].iloc[i]:

        data_compra.append(dataSet.iloc[i+1].name) # +1 porque a gente compra no preço de abertura do dia seguinte.

        for j in range(1, 11):

            if dataSet['RSI'].iloc[i + j] > 40: #vendo se nos proximos 10 dias o RSI passa de 40

                data_venda.append(dataSet.iloc[i + j + 1].name) #vende no dia seguinte q bater 40
                break

            elif j == 10:
                data_venda.append(dataSet.iloc[i + j + 1].name)

lucros = dataSet.loc[data_venda]['bid'].values/dataSet.loc[data_compra]['bid'].values - 1
performance_acumulada = (np.cumprod((1 + lucros)) - 1)


# import matplotlib.animation as anim


fig, ax = plt.subplots(figsize=(12, 5))

# ax.scatter(dataSet.loc[data_compra].index, dataSet.loc[data_compra]['last'], marker = '^',
#             c = 'g')
# ax.plot(dataSet['last'], alpha = 0.7)

def update(i):
    ax.clear()
    ax.scatter(dataSet.loc[data_compra].index, dataSet.loc[data_compra]['last'], marker = '^', c = 'g')
    ax.plot(dataSet['last'], alpha = 0.7)
    plt.pause(0.1)

#plt.show()

import time
import random
tempVal = 0


while True:
	#dataSet['last'] = dataSet['last'].apply(lambda x: random.uniform(0.5, 1)+x)
	update(tempVal)
	time.sleep(5)
	print("ATUALIZA")

