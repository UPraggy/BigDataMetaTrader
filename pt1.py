#npx nodemon --exec "clear;python3" main.py
import MetaTrader5 as mt5
import os
from datetime import datetime
os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize() #inicializar


terminal = mt5.terminal_info()._asdict() #Apresentando opções do terminal

ativoSelecionado = "EURUSD" #Selecionando Ativo

#date_from -> timestamp
#copy_ticks_from(symbol, date_from, count, flags)

date = datetime(2023,8,18) #Selecionando tempo
flags = mt5.COPY_TICKS_ALL #Pegando todas as variações no preço 

dataSet = mt5.copy_ticks_from(ativoSelecionado, 
			date, 10, flags)


#print(dataSet)
#print(dataSet.dtype) 

import pandas as pd

dataSetDF = pd.DataFrame(dataSet)

print(dataSetDF["time"])



mt5.shutdown()