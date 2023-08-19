## Incializar MT5

```python
import MetaTrader5 as mt5
import os
from datetime import datetime
os.system('cls' if os.name == 'nt' else 'clear')

mt5.initialize() #inicializar
```

## Listar ativos
#### Comando lento, pois retornar diversos itens
```python

ativos = mt5.symbols_get()

print([x.name for x in ativos])
```

## Selecionando ativo, filtrando informações e direcionando a um DataFrame

```python
ativoSelecionado = "EURUSD" #Selecionando Ativo

#date_from -> timestamp
#copy_ticks_from(symbol, date_from, count, flags)

date = datetime(2023,8,18) #Selecionando tempo
flags = mt5.COPY_TICKS_ALL #Pegando todas as variações no preço 

dataSet = mt5.copy_ticks_from(ativoSelecionado, 
			date, 10, flags)

import pandas as pd

dataSetDF = pd.DataFrame(dataSet)

print(dataSetDF)
```











