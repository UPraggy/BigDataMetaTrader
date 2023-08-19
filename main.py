import MetaTrader5 as mt5
import os
from datetime import datetime
os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize() #inicializar


terminal = mt5.terminal_info()._asdict() #Apresentando opções do terminal


#ativos = mt5.symbols_get()

#print([x.name for x in ativos])

EURUSD = mt5.symbol_info("EURUSD")

print(EURUSD._asdict()) # Convertendo para dicionário


mt5.shutdown()