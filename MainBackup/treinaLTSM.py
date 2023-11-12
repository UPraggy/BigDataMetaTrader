import pandas as pd;
from sklearn.preprocessing import MinMaxScaler;
from keras.models import Sequential;
from keras.layers import Dense, LSTM;
import matplotlib.pyplot as plt;
from datetime import datetime;
from datetime import timedelta;
import numpy as np

def treinaLTSM(dataSet):
	testeDATA = dataSet.copy()
	cotacao = testeDATA['last'].to_numpy().reshape(-1, 1);

	# print(cotacao);

	tamanho_dados_treinamento = int(len(cotacao) * 0.8);



	# Escalador os dados entre 0 e 1, para deixar mais facil o processamento
	# dados em escala pré definidas são mais fáceis de lidar

	escalador = MinMaxScaler(feature_range=(0, 1));

	dados_entre_0_e_1_treinamento = escalador.fit_transform(cotacao[0: tamanho_dados_treinamento, :]);
	dados_entre_0_e_1_teste = escalador.transform(cotacao[tamanho_dados_treinamento: , : ]);

	dados_entre_0_e_1 = list(dados_entre_0_e_1_treinamento.reshape(
	    len(dados_entre_0_e_1_treinamento))) + list(dados_entre_0_e_1_teste.reshape(len(dados_entre_0_e_1_teste)));

	dados_entre_0_e_1 = np.array(dados_entre_0_e_1).reshape(len(dados_entre_0_e_1), 1);



	dados_para_treinmaneto = dados_entre_0_e_1[0: tamanho_dados_treinamento, :];

	#dados que serão usados para gerar o resultado
	treinamento_x = [];

	#cotação que aconteceu de fato
	treinamento_y = [];

	for i in range(60, len(dados_para_treinmaneto)):

	    #60 ultimos dias
	    treinamento_x.append(dados_para_treinmaneto[i - 60: i, 0]);

	    #cotacao
	    treinamento_y.append(dados_para_treinmaneto[i, 0]);

	    # if i <= 61:
	    #     print(treinamento_x);
	    #     print(treinamento_y);


	#transformando as listas em arrays e dando reshape 3d

	treinamento_x, treinamento_y = np.array(treinamento_x), np.array(treinamento_y);

	treinamento_x = treinamento_x.reshape(treinamento_x.shape[0], treinamento_x.shape[1], 1);



	#contruindo o modelo

	modelo = Sequential()

	#camos criar um modelo com 50 neurônios
	#return sequences = True pois vamos usar outra LSTM depois.
	#definir o shap, que no caso são 60 informações para gerar uma.
	#Adicionar mais neurônios com o dense, 25 e 1
	#Nâo se apegue a isso agora, é apenas uma arquitetura de deep learning

	modelo.add(LSTM(50, return_sequences=True, input_shape = (treinamento_x.shape[1], 1)));
	modelo.add(LSTM(50, return_sequences=False));
	modelo.add(Dense(25));
	modelo.add(Dense(1));



	#copilando o modelo

	#a função de loss é a forma de medir o erro do modelo, que nesse caso
	#é o classico erro médio quadrático da que é usada em regressão linear
	#otimizador e medida de erro

	modelo.compile(optimizer="adam", loss="mean_squared_error");

	#agora com o modelo copilado e os dados, podemos treinar o modelo
	#batch size é depois de quantas em quantas amostras o modelo irá otimizar os parâmetros.
	#epochs é quantas vezes o algoritmo irá rodar os dados trinamento, aprendendo

	modelo.fit(treinamento_x, treinamento_y, batch_size=1, epochs=1);


	#criar dados de teste

	dados_teste = dados_entre_0_e_1[tamanho_dados_treinamento - 60:, :];

	teste_x = [];
	teste_y = cotacao[tamanho_dados_treinamento: , :];

	for i in range(60, len(dados_teste)):
	    teste_x.append(dados_teste[i - 60: i, 0]);

	# reshape
	teste_x = np.array(teste_x);
	teste_x = teste_x.reshape(teste_x.shape[0], teste_x.shape[1], 1);


	# pegando predições do modelo

	predicoes = modelo.predict(teste_x);

	# tirando a escala dos dados

	predicoes = escalador.inverse_transform(predicoes);

	# print(predicoes)


	#pegando o erro médio quadrático

	rmse = np.sqrt(np.mean(predicoes - teste_y) ** 2)



	#criando o grafico modelo

	treinamento = testeDATA.iloc[:tamanho_dados_treinamento, :]
	df_teste = pd.DataFrame({"Close": testeDATA['last'].iloc[tamanho_dados_treinamento:] ,
	                         "predicoes": predicoes.reshape(len(predicoes))})


	#O preço é legal, mas o importante é acertar pra qual mercado o lado vai. será que isso foi feito?
	# Calcular media de acertos e expectativa de lucro

	df_teste['variacao_percentual_acao'] = df_teste['Close'].pct_change()
	df_teste['variacao_percentual_modelo'] = df_teste['predicoes'].pct_change()

	df_teste = df_teste.dropna()

	df_teste['var_acao_maior_menor_que_zero'] = np.where(df_teste['variacao_percentual_acao'] > 0, True, False)
	df_teste['var_modelo_maior_menor_que_zero'] = np.where(df_teste['variacao_percentual_modelo'] > 0, True, False)

	df_teste['acertou_o_lado'] = np.where(df_teste['var_acao_maior_menor_que_zero'] == df_teste['var_modelo_maior_menor_que_zero'], True, False)

	df_teste['variacao_percentual_acao_abs'] = df_teste['variacao_percentual_acao'].abs()

	# print(df_teste)

	acertou_lado = df_teste['acertou_o_lado'].sum()/len(df_teste['acertou_o_lado'])
	errou_lado = 1 - acertou_lado

	media_lucro = df_teste.groupby('acertou_o_lado')['variacao_percentual_acao_abs'].mean()

	exp_mat_lucro = acertou_lado * media_lucro[1] - media_lucro[0] * errou_lado

	ganho_sobre_perda = media_lucro[1]/media_lucro[0]
	print("Treinou")
	return [modelo,escalador]
