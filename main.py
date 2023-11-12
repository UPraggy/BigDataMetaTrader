import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import time
import os

from getCarteira import getCarteira 
from getPrevisaoModel import getPrevisaoModel, getNovaPrevisaoModel
from getAtivosDF import geraDFAtivos
from configuraCompra import trataDF, configuraBaseCompra, configuraBaseUltimoIndice
from lstmConfigure import LSTMFunc

os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize(login=612347195,server='XPMT5-DEMO',password="PassTeste1()()") #inicializar


#melhorCarteira = getCarteira(mt5)




import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import time
#['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'ativo', 'EBIT', 'ROIC', 'ranking_ev_ebit']

#dataSet = geraDFAtivos(melhorCarteira,horasDif=10*24)
dataSet = geraDFAtivos('AAPL34',horasDif=10*24)
#DATAFRAME COMPLETO
dataSet = trataDF(dataSet)

dataSet['mes_dia'] = dataSet.index.strftime('%m-%d')

# Para obter a lista de chaves em ordem
dias = list(dataSet.groupby('mes_dia').groups.keys())

#pegando dois dias antes
[x_trainT1, y_trainT1, modelT1,scalerT1] = LSTMFunc(dataSet, int(dias[-3:-2][0].split('-')[1]))

# NovaPrevT3 = getPrevisaoModel(dataSet, scalerT1, modelT1,dias)


dataSetFinal = dataSet.loc[(dataSet.index.day == int(dias[-3:-2][0].split('-')[1]))].copy()

# @title Simulação Tempo Real
#criando simulacao de um dataframe com os tempos futuros
futureDataSet = dataSetFinal[1:].copy()

#criando simulacao de um dataframe com os tempos atuais
dataSetAtual = dataSetFinal.iloc[:1].copy()


tempoFuturo = 1
compraAtual = 0

compraTotal = []
vendaTotal = []


limiteTempoSemVender = 0

from treinoNovo import atualizaPrev 

fig, ax = plt.subplots(figsize=(12, 5))

def update(dataSetAtual,compraTotal,vendaTotal):
    ax.clear()
    ax.scatter([i["x"] for i in compraTotal], [i["y"] for i in compraTotal], marker = 'o', c = 'r', label='compraTotal')
    ax.scatter([i["x"] for i in vendaTotal], [i["y"] for i in vendaTotal], marker = 'o', c = 'g', label='vendaTotal')
    ax.plot(dataSetAtual['last'], alpha = 0.7, label='Previsao')
    ax.legend()
    plt.pause(0.001)


while True:
  if (tempoFuturo == len(futureDataSet)-2):
      break
   # transpose convertendo para que dê para juntar no dataframe atual
  tmp = futureDataSet.iloc[tempoFuturo].to_frame().transpose()
 
   #adicionando linha do futuro
  dataSetAtual = pd.concat([dataSetAtual,tmp])
  indiceElAtual = (dataSetAtual.shape[0] - 1)

  valorFuturo = 0
  valorAtual = 0

  #por ser base offline a compra terá um delay, ou seja, compra um minuto depois
  valorAtualReal = futureDataSet.iloc[(indiceElAtual+1)]['last']
  
  [x_trainT1,y_trainT1, scalerT1,modelT1] = atualizaPrev(
    dataSet.loc[dataSet.index <=  dataSetAtual.index[-1]].copy(), x_trainT1, y_trainT1)

  NovaPrevT3 = getNovaPrevisaoModel(dataSet, scalerT1, modelT1,dias, x_trainT1)

  dataSetAtual.at[dataSetAtual.index[-1], 'Previsao'] = NovaPrevT3[-1]


  #AQUI COMPRA
  if (valorFuturo <= (valorAtual*0.99998) and compraAtual == 0):
    compraTotal.append({"x": futureDataSet.iloc[(indiceElAtual+1)].name, "y": valorAtualReal})
    compraAtual = valorAtualReal
    #print("COMPRA",futureDataSet.iloc[(indiceElAtual+1)].name, valorAtualReal, limiteTempoSemVender)

  #AQUI VENDE
  if (compraAtual > 0):
      if((valorAtualReal > compraAtual*1.0001) or (limiteTempoSemVender >= 30
          and (valorAtualReal == compraAtual))  or (valorAtualReal < compraAtual*0.99995)):
          #print("VENDA",futureDataSet.iloc[(indiceElAtual+1)].name, valorAtualReal, limiteTempoSemVender)
          limiteTempoSemVender = 0
          compraAtual = 0
          vendaTotal.append({"x": futureDataSet.iloc[(indiceElAtual+1)].name, "y": valorAtualReal})
  else:
        limiteTempoSemVender += 1


  update(dataSetAtual,compraTotal,vendaTotal)
  tempoFuturo += 1
  time.sleep(0.001)





compraSoma = sum([d['y'] for d in compraTotal])
vendaSoma = sum([d['y'] for d in vendaTotal])


ax.scatter([i["x"] for i in compraTotal], [i["y"] for i in compraTotal], marker = 'o', c = 'r', label='compraTotal')
ax.scatter([i["x"] for i in vendaTotal], [i["y"] for i in vendaTotal], marker = 'o', c = 'g', label='vendaTotal')
ax.plot(dataSetAtual['Previsao'], alpha = 0.7, label='Previsao')
ax.plot(dataSetAtual['last'], alpha = 0.7, label='Real')
ax.legend()
print("COMPRA TOTAL")
print(compraSoma)
print("VENDA TOTAL")
print(vendaSoma)

print("LUCRO")
print(vendaSoma-compraSoma)#+compraTotal[-1]['y'])

plt.show()




















'''  
import plotly.graph_objects as go

fig = go.Figure()


fig.add_trace(go.Scatter(x=futureDataSet.index,
                         y=futureDataSet['Previsao'], name='Previsao'))

fig.add_trace(go.Scatter(x=[i["x"] for i in compraTotal],
                         y=[i["y"] for i in compraTotal], mode='markers', name='Compra'))

fig.add_trace(go.Scatter(x=[i["x"] for i in vendaTotal],
                         y=[i["y"] for i in vendaTotal], mode='markers', name='Venda'))
# Exibição da figura
fig.show()'''