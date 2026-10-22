# TRABAJO AGRÍCOLA EN CHILE

# Prefácio: Instalar ferramentas básicas necessárias
library(readxl)
library(ggplot2)
library(dplyr)
library(scales) # Formata os números

#-----------------------------------------------------------
# Capítulo 1: Ler a planilha limpa
dados <- read_excel("base_agricola_limpa_2020_2021.xlsx")

#-----------------------------------------------------------
# Capítulo 2: Filtra o "Total Nacional" e as Top 5 regiões
dados_grafico <- dados %>% 
  filter(Regiao != "Total Nacional") %>% 
  arrange(desc(Total_Trabalhadores_Temporarios)) %>% 
  head(5)

#-----------------------------------------------------------
# Capítulo 3: Criar o gráfico de barras
ggplot(dados_grafico, aes(x = reorder(Regiao, Total_Trabalhadores_Temporarios), y = Total_Trabalhadores_Temporarios)) + 
  geom_bar(stat = "identity", fill = "darkorchid") + 
  
  # Adiciona os rótulos de dados dentro das barras
  geom_text(aes(label = scales::comma(Total_Trabalhadores_Temporarios, big.mark = ".", decimal.mark = ",")), 
            hjust = 1.1, color = "white", size = 4, fontface = "bold") +
  
  coord_flip() + 
  
  # Formata o eixo para remover a notação científica
  scale_y_continuous(labels = scales::comma_format(big.mark = ".", decimal.mark = ",")) +
  
  labs( 
    title = "Top 5 Regiões do Chile em Emprego Agrícola Temporário", 
    subtitle = "Temporada 2020/2021", 
    x = NULL, # Omitido para não repetir a palavra "Região"
    y = "Número de Trabalhadores Temporários" 
  ) + 
  theme_minimal()