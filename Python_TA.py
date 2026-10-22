# TRABAJO AGRÍCOLA EN CHILE 2020/2021

# Prefácio: Importação de bibliotecas e derivados basilares.
import pandas as pd # Manipular e limpar planilhas
import requests # Responsável pela API
from selenium import webdriver # Responsável pelo Web-Scraping
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Projeto Piloto de Pesquisa Econômica ---\n Trabalho Agrícola no Chile em 2020/2021")

# -----------------------------------------------------------
# Capítulo 1: Manipular e limpar dados

print("I. Limpando os dados da planilha Trabalho Agrícola do Excel...")

# Especificar qual aba e linhas estou analisando.
df = pd.read_excel("trabajo-agrícola.xlsx", sheet_name='16', skiprows=5)

# Limpar coluna e remover células vazias
df = df.dropna(subset=['Unnamed: 1']) 
df = df.rename(columns={
    'Unnamed: 1': 'Regiao', 
    'Total': 'Total_Trabalhadores_Permanentes',
    'Total.1': 'Total_Trabalhadores_Temporarios'
})

# Filtro variáveis de interesse 
df_filtrado = df[['Regiao', 'Total_Trabalhadores_Permanentes', 'Total_Trabalhadores_Temporarios']]

# Divulga total nacional
# iloc: Integer Location
total_permanentes = df_filtrado.iloc[0]['Total_Trabalhadores_Permanentes']
total_temporarios = df_filtrado.iloc[0]['Total_Trabalhadores_Temporarios']
print(f"-> Total de Trabalhadores Permanentes : {total_permanentes}")
print(f"-> Total de Trabalhadores Temporários : {total_temporarios}\n")

# -----------------------------------------------------------
# Capítulo 2: Utilizando API com dados do Banco Mundial

print("II. Coletando dados macroeconômicos divulgados no Banco Mundial via API...")
# Busco % da Agricultura no PIB do Chile 
# Código do Chile: CHL
# Código do indicador do Banco Mundial: NV.AGR.TOTL.ZS
# Aplico silgas específicas no link base disponível no Banco Mundial
url_api = "https://api.worldbank.org/v2/country/CHL/indicator/NV.AGR.TOTL.ZS?format=json"

# Função .get da biblioteca Requests para buscar e armazenar informações 
resposta = requests.get(url_api)
# Função .json da biblioteca Requests traduz dados em JSON para listas e bibliotecas para que o Python leia
dados_api = resposta.json()

# Extraio o dado mais recente disponível
# [0] contém data e [1], o dado percentual
dado_pib_agricola = dados_api[1][0]['value'] 
ano_dado = dados_api[1][0]['date']
print(f"-> A agricultura representou {dado_pib_agricola:.2f}% do PIB do Chile no ano de {ano_dado}.\n")

# -----------------------------------------------------------
# Capítulo 3: Web-scraping com Selenium no INE
print("III. Iniciando o Selenium para extrair dados em tempo real do INE...")

# Abre um navegador fantasma automaticamente
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Mando o selenium entrar no site do Censo Agropecuario
url_ine = "https://www.ine.gob.cl/estadisticas-por-tema/agricultura-y-medio-ambiente/censo-agropecuario"
navegador.get(url_ine)

# Tempo de descanso para não pegar dados erroneos por erro no carregamento da página
time.sleep(5)

# Peço ao robô que procure e copie o texto dos indicadores que estão na tela
try:
    # Procura elementos no site que contêm as estatísticas
    # Nota: XPaths podem mudar, esta é uma busca genérica baseada na estrutura de sites do governo
    indicadores = navegador.find_elements(By.CLASS_NAME, "indicator-value") 
    titulos = navegador.find_elements(By.CLASS_NAME, "indicator-title")
    
    print("-> Dados extraídos do site via Scraping:")
    for i in range(min(len(indicadores), 3)): # Pegar os 3 primeiros
        print(f"   * {titulos[i].text}: {indicadores[i].text}")
except Exception as e:
    print("-> Nota: Os indicadores dinâmicos não estavam visíveis ou a estrutura do site mudou.")

# Fecho o navegador fantasma
navegador.quit()

print("Coleta e manipulação dos dados realizada com sucesso!")
# Salva tudo em um novo Excel: df_limpo.to_excel("Dados_Finais_Limpos.xlsx")
df_filtrado.to_excel("Base_Agricola_Limpa_2020_2021.xlsx", index=False)