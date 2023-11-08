import pandas as pd 

import pandas as pd

def trataDF(dadosAtivo):
    # Converte milissegundos para minutos e depois para datetime
    #minutos .apply(lambda x : x/60000), unit='m')
    #segundos .apply(lambda x : x/1000), unit='s')
    dadosAtivo['time'] = pd.to_datetime(dadosAtivo['time_msc'].apply(lambda x : x/60000), unit='m')


    # Certifique-se de que 'time' é o índice
    dadosAtivo.set_index('time', inplace=True)

    dadosAtivo = dadosAtivo.loc[(dadosAtivo.index.weekday >= 0) & (dadosAtivo.index.weekday < 5)]
    dadosAtivo = dadosAtivo.loc[(dadosAtivo.index.hour >= 10) & ((dadosAtivo.index.hour < 17) )]

    # Define as funções de agregação para cada coluna
    aggregations = {
        'volume': 'sum',  # soma
        'flags': 'sum',  # soma
        'bid': 'mean',   # média
        'ask': 'mean',   # média
        'last': 'mean'   # média
    }

    # Agrupa por minuto e aplica as funções de agregação
    dadosAtivo = dadosAtivo.resample('1T').agg(aggregations)

    # Remove casas decimais ou diminui elas, onde é necessário
    dadosAtivo[['bid','ask','last']] = dadosAtivo[['bid','ask','last']].apply(lambda x : round(x,2))
    dadosAtivo[['volume','flags']] =  dadosAtivo[['volume','flags']].astype('int64')
    dadosAtivo = dadosAtivo.loc[dadosAtivo['volume'] != 0]

    return dadosAtivo

def configuraBaseCompra(dadosAtivo): 
    
    #Calculando retorno percentual baseado na coluna e usou o dropna para apagar os valores nulos
    dadosAtivo['retornos'] = dadosAtivo['last'].pct_change()

    #Separa os retornos e já calcula a média
    dadosAtivo['retornosPostivos'] = dadosAtivo['retornos'].apply(lambda x: x if x > 0 else 0).rolling(window = 22, min_periods=2).mean() # se retorno maior que 0, é retorno positivo

    dadosAtivo['retornosNegativos'] = dadosAtivo['retornos'].apply(lambda x: abs(x) if x < 0 else 0).rolling(window = 22, min_periods=2).mean()

    #Calculando RSI -> se baseia no quanto ele tende a ficar positivo ou negativo
    dadosAtivo['RSI'] = (100 - 100/
                            (1 + dadosAtivo['retornosPostivos']/dadosAtivo['retornosNegativos']))

    dadosAtivo = dadosAtivo.loc[dadosAtivo['RSI'].notnull()]

    dfTMP = dadosAtivo['RSI'].apply(lambda x: "sim" if x < 30 else "nao")
   
    #tirando mensagem de erro de copia
    dfTMP = dfTMP.rename("compra", inplace=True)

    return pd.merge(dadosAtivo,dfTMP,left_index=True, right_index=True)


def configuraBaseUltimoIndice(dadosAtivo): 

    #dadosAtivo.loc[dadosAtivo.index[-1], 'coluna'] tirando erro de copia

    #Calculando retorno percentual baseado na coluna
    dadosAtivo.loc[dadosAtivo.index[-1], 'retornos'] = dadosAtivo['last'].tail(5).pct_change().iloc[-1]

    #Separa os retornos e já calcula a média
    dadosAtivo.loc[dadosAtivo.index[-1], 'retornosPostivos'] = dadosAtivo['retornos'].tail(25).apply(lambda x: x if x > 0 else 0).rolling(window = 22, min_periods=2).mean().iloc[-1].copy() # se retorno maior que 0, é retorno positivo

    dadosAtivo.loc[dadosAtivo.index[-1], 'retornosNegativos'] = dadosAtivo['retornos'].tail(25).apply(lambda x: abs(x) if x < 0 else 0).rolling(window = 22, min_periods=2).mean().iloc[-1].copy()

    #Calculando RSI -> se baseia no quanto ele tende a ficar positivo ou negativo
    dadosAtivo.loc[dadosAtivo.index[-1], 'RSI'] = (100 - 100/
                            (1 + dadosAtivo['retornosPostivos'].iloc[-1]/dadosAtivo['retornosNegativos'].iloc[-1]))

    dadosAtivo = dadosAtivo.loc[dadosAtivo['RSI'].notnull()]

    dadosAtivo.loc[dadosAtivo.index[-1], 'compra'] = (lambda x: "sim" if x < 30 else "nao")(dadosAtivo['RSI'].iloc[-1])

    return dadosAtivo