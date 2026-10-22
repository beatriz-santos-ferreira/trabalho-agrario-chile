# TRABAJO AGRÍCOLA EN CHILE 2020/2021

# Prefácio: Importação de bibliotecas e derivados basilares.
import pandas as pd
import requests # Para a API
from selenium import webdriver # Para o Web-Scraping
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Projeto Piloto de Pesquisa Econômica ---\n Trabalho Agrícola no Chile em 2020/2021")

# FASE 1: MANIPULAÇÃO DE DADOS (SEU EXCEL)
print("1. Limpando os dados de Trabalho Agrícola do Excel...")

# Lemos a planilha pulando as 5 primeiras linhas que estão vazias/bagunçadas
df = pd.read_excel("trabajo-agrícola.xlsx", sheet_name='16', skiprows=5)

# Limpamos as colunas e removemos linhas vazias
df = df.dropna(subset=['Unnamed: 1']) 
df = df.rename(columns={
    'Unnamed: 1': 'Regiao', 
    'Total': 'Total_Trabalhadores_Permanentes',
    'Total.1': 'Total_Trabalhadores_Temporarios'
})
# Selecionamos apenas as colunas que importam para o modelo econômico
df_limpo = df[['Regiao', 'Total_Trabalhadores_Permanentes', 'Total_Trabalhadores_Temporarios']]

# Mostramos o total nacional (que é a primeira linha)
total_permanentes = df_limpo.iloc[0]['Total_Trabalhadores_Permanentes']
total_temporarios = df_limpo.iloc[0]['Total_Trabalhadores_Temporarios']
print(f"-> Total de Trabalhadores Permanentes (Chile): {total_permanentes}")
print(f"-> Total de Trabalhadores Temporários (Chile): {total_temporarios}\n")


# ==========================================
# FASE 2: API RESEARCH (BANCO MUNDIAL)
# ==========================================
print("2. Coletando dados macroeconômicos via API (Banco Mundial)...")
# Vamos buscar a % da Agricultura no PIB do Chile (Código do país: CHL)
# Código do indicador do Banco Mundial: NV.AGR.TOTL.ZS
url_api = "https://api.worldbank.org/v2/country/CHL/indicator/NV.AGR.TOTL.ZS?format=json"

resposta = requests.get(url_api)
dados_api = resposta.json()

# Extraindo o dado mais recente disponível
dado_pib_agricola = dados_api[1][0]['value'] 
ano_dado = dados_api[1][0]['date']
print(f"-> A agricultura representou {dado_pib_agricola:.2f}% do PIB do Chile no ano de {ano_dado}.\n")


# ==========================================
# FASE 3: WEB-SCRAPING (SELENIUM) - SITE DO INE
# ==========================================
print("3. Iniciando o Robô (Selenium) para extrair dados em tempo real do INE...")

# Isso vai abrir um navegador fantasma automaticamente
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Mandamos o robô entrar no site do Censo Agropecuario
url_ine = "https://www.ine.gob.cl/estadisticas-por-tema/agricultura-y-medio-ambiente/censo-agropecuario"
navegador.get(url_ine)

# Esperamos 5 segundos para a página carregar completamente
time.sleep(5)

# Pedimos ao robô para procurar e copiar o texto dos indicadores que estão na tela
try:
    # O código abaixo procura elementos no site que contêm as estatísticas
    # Nota: XPaths podem mudar, esta é uma busca genérica baseada na estrutura de sites do governo
    indicadores = navegador.find_elements(By.CLASS_NAME, "indicator-value") 
    titulos = navegador.find_elements(By.CLASS_NAME, "indicator-title")
    
    print("-> Dados extraídos do site via Scraping:")
    for i in range(min(len(indicadores), 3)): # Pegar os 3 primeiros
        print(f"   * {titulos[i].text}: {indicadores[i].text}")
except Exception as e:
    print("-> Nota: Os indicadores dinâmicos não estavam visíveis ou a estrutura do site mudou.")

# Fechamos o navegador fantasma
navegador.quit()

print("\n--- COLETA E MANIPULAÇÃO CONCLUÍDAS COM SUCESSO! ---")
# Aqui você pode salvar tudo num novo Excel se quiser: df_limpo.to_excel("Dados_Finais_Limpos.xlsx")
df_limpo.to_excel("Base_Agricola_Limpa_2025.xlsx", index=False)