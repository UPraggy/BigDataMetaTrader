
def configuraBaseCompra(dadosAtivo,ativoSelecionado): 
    #seleciona ativo
    dadosAtivo = dadosAtivo.loc[dadosAtivo['ativo'] == ativoSelecionado]

    #agrupa por tempo de forma a não ter dados "duplicados" pegando a média deles, ou seja, com mesma hora
    dadosAtivo = dadosAtivo.groupby('time').aggregate(lambda x : x.iloc[0] if x.dtype == 'object' else x.mean())

    print(dadosAtivo)
    #remove casas decimais ou diminui elas, onde é necessário
    dadosAtivo[['bid','ask','last']] = dadosAtivo[['bid','ask','last']].apply(lambda x : round(x,2))
    dadosAtivo[['volume','flags','volume_real','time_msc']] =  dadosAtivo[['volume','flags','volume_real','time_msc']].astype('int64')

    #Calculando retorno percentual baseado na coluna e usou o dropna para apagar os valores nulos
    dadosAtivo['retornos'] = dadosAtivo['last'].pct_change()

    #Separa os retornos e já calcula a média
    dadosAtivo['retornosPostivos'] = dadosAtivo['retornos'].apply(lambda x: x if x > 0 else 0).rolling(window = 22).mean() # se retorno maior que 0, é retorno positivo
    dadosAtivo['retornosNegativos'] = dadosAtivo['retornos'].apply(lambda x: abs(x) if x < 0 else 0).rolling(window = 22).mean()

    #Calculando RSI -> se baseia no quanto ele tende a ficar positivo ou negativo
    dadosAtivo['RSI'] = (100 - 100/
                            (1 + dadosAtivo['retornosPostivos']/dadosAtivo['retornosNegativos']))

    dadosAtivo = dadosAtivo.loc[dadosAtivo['RSI'].notnull()]

    

    dadosAtivo['compra'] = dadosAtivo['RSI'].apply(lambda x: "sim" if x < 30 else "nao")

    

    return dadosAtivo
