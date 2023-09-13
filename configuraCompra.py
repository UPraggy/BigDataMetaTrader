import pandas as pd 

def trataDF(dadosAtivo,ativoSelecionado):
    #seleciona ativo
    dadosAtivo = dadosAtivo.loc[dadosAtivo['ativo'] == ativoSelecionado]
    #agrupa por tempo de forma a não ter dados "duplicados" pegando a média deles, ou seja, com mesma hora

    dadosAtivo = dadosAtivo.groupby('time').aggregate(lambda x : x.iloc[0] if x.dtype == 'object' else x.mean())

    #remove casas decimais ou diminui elas, onde é necessário
    dadosAtivo[['bid','ask','last']] = dadosAtivo[['bid','ask','last']].apply(lambda x : round(x,2))
    dadosAtivo[['volume','flags','volume_real','time_msc']] =  dadosAtivo[['volume','flags','volume_real','time_msc']].astype('int64')

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