import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import time
import os

from getCarteira import getCarteira 
from getAtivosDF import geraDFAtivos
from configuraCompra import trataDF, configuraBaseCompra, configuraBaseUltimoIndice
from treinaLTSM import treinaLTSM


os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar


simbols = [x.name for x in mt5.symbols_get() if "BOVESPA\\A VISTA" in x.path ]

melhorCarteira = 'CEAB3'#getCarteira(mt5)




dataSet = geraDFAtivos(melhorCarteira,horasDif=5*24)

#DATAFRAME COMPLETO
dataSet = trataDF(dataSet, melhorCarteira)
dataSetTreino = treinaLTSM(dataSet)


[modelo,escalador] = dataSetTreino
cotacoes = dataSet.copy()
ultimos_60_dias = cotacoes.iloc[-500:]['last'].values.reshape(-1, 1)

ultimos_60_dias_escalado = escalador.transform(ultimos_60_dias)

teste_x = []
teste_x.append(ultimos_60_dias_escalado)
teste_x = np.array(teste_x)
teste_x = teste_x.reshape(teste_x.shape[0], teste_x.shape[1], 1)


previsao_de_preco = []
previsao_de_preco = np.append(previsao_de_preco,modelo.predict([teste_x[0]]))


previsao_de_preco = escalador.inverse_transform([previsao_de_preco])


# @title Ajustando diferença e mostrando preço real
print(np.mean(previsao_de_preco[0][-200:]))
print(cotacoes.tail(200)['last'].mean())
diferencaPrevEReal = cotacoes.tail(200)['last'].mean() - np.mean(previsao_de_preco[0][-200:])
print(diferencaPrevEReal)
NovaPrev = []
for x in range(len(previsao_de_preco[0])):
   NovaPrev.append(previsao_de_preco[0][x] + diferencaPrevEReal)



# Configurando para grafico não completar periodo faltante
TMP_contacoes_previsao = cotacoes.copy()
TMP_contacoes= dataSet.iloc[-500:].copy()
TMP_contacoes_previsao.index = TMP_contacoes_previsao.index.strftime('%Y-%m-%d %H:%M:%S')
TMP_contacoes.index = TMP_contacoes.index.strftime('%Y-%m-%d %H:%M:%S')


# # Criação da figura

import plotly.graph_objects as go

fig = go.Figure()



#fig.add_trace(go.Scatter(x=TMP_contacoes.index, y=TMP_contacoes['last'], name='Dados Originais'))
fig.add_trace(go.Scatter(x=TMP_contacoes_previsao.iloc[-500:].index, y=previsao_de_preco[0], name='Previsão de Preço'))
fig.add_trace(go.Scatter(x=TMP_contacoes_previsao.iloc[-500:].index, y=NovaPrev, name='Previsão de Preço Ajustada'))
fig.add_trace(go.Scatter(x=dataSet.copy().index,
                         y=dataSet.copy()['last'], name='Valor Real'))

# Exibição da figura
fig.show()