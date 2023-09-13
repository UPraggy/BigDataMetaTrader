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


# Pegar Dados EBIT e ROIC 
## Selecionando google finances

```python
import requests
from bs4 import BeautifulSoup
ativo = 'PETR4'
linkAtivoGoogle = 'PETR4:BVMF'

site = f'https://www.google.com/finance/quote/{linkAtivoGoogle}'
response = requests.get(site)

if response.status_code == 200:
    html = response.text
    titleCortado = 'Artigo detalhando '
    # Cria um objeto BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html, 'html.parser')

    #Pegando os Valores por codigo (Trismestral)
    EBIT = soup.find_all('div',id='incomeStatementTT4')
    EBIT = EBIT[0].parent.parent.parent.find_all('span', class_='JwB6zf Ebnabc CnzlGc')
    EBIT = EBIT[0].get_text()

    ROIC = soup.find_all('div',id='balanceSheetTT7')
    ROIC = ROIC[0].parent.parent.parent.find_all('td', class_='QXDnM')
    ROIC = ROIC[0].get_text()
    print(f'EBIT {eBIT} / ROIC {ROIC}')

else:
    print("Erro ao fazer a requisição")
```


# Compra com parametros necessários
#### Para usar em um determinado tempo, deverá ser utilizada uma comparação

```python
result = mt5.order_send({
    "action" : mt5.TRADE_ACTION_DEAL,
    "symbol" : "PETR4" # ação desejada
    "volume" : 0.0001 # 100 unidades da ação corrente
    "price"  : mt5.symbol_info_tick(symbol).ask, # Preço (neste exemplo, é o preço atual)
    "type"   : mt5.ORDER_TYPE_BUY, # Tipo de ordem (compra)
    "comment": "Compra via python",
    })

```








