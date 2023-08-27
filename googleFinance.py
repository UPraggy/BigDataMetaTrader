import requests
from bs4 import BeautifulSoup

def getEBIT_ROIC(ativos):
	#Lista de Ativos
	#[{ativo = '', linkAtivoGoogle = ''},{ativo = 'PETR4', linkAtivoGoogle = 'PETR4:BVMF'}]
	objetoFinal = {}

	for ativo in ativos:
		site = f'https://www.google.com/finance/quote/{ativo["linkAtivoGoogle"]}'
		response = requests.get(site)
		
		if response.status_code == 200:
		    html = response.text
		    titleCortado = 'Artigo detalhando '
		    # Cria um objeto BeautifulSoup para analisar o HTML
		    soup = BeautifulSoup(html, 'html.parser')

		    #Pegando os Valoresr codigo (Trismestra pol)
		    EBIT = soup.find_all('div',id='incomeStatementTT4')
		    EBIT = EBIT[0].parent.parent.parent.find_all('span', class_='JwB6zf')
		    EBIT = EBIT[0].get_text()

		    ROIC = soup.find_all('div',id='balanceSheetTT7')
		    ROIC = ROIC[0].parent.parent.parent.find_all('td', class_='QXDnM')
		    ROIC = ROIC[0].get_text()
		    objetoFinal[ativo["ativo"]] = {'EBIT': EBIT, 'ROIC': ROIC} 

		else:
		    print("Erro ao fazer a requisição")
		    objetoFinal[ativo["ativo"]] = {'EBIT': none, 'ROIC': none} 
	return objetoFinal