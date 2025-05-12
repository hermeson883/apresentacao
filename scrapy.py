import os
import re
import time
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument('--headless=new')

browser = webdriver.Chrome()  # Criando a instância do chrome

# Site para fazer o scrap
browser.get("https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas")  

browser.find_element(By.TAG_NAME, "body").click()  #Clicando em algum elemento da página

browser.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div/div[2]/button[2]").click()  # Clicando para recusar os coockies da sessão

time.sleep(3)  # Aguardando os elementos da página sumirem

gas_price = browser.find_element(By.XPATH, '//*[@id="parent-fieldname-text"]/ul[2]/li[1]/a')  # Encontrando o arquivo desejado

gas_price.click() # Fazendo o download do arquivo

sleep(5)

path = os.path.expanduser("~") # Caminho para poder selecionar os arquivos

path = path + r"\Downloads" # Unindo o caminho base com o caminho de downloads

href = gas_price.get_attribute("href")  # pegando o hiper link da planilha

match_string = re.search("resumo_semanal.*$", href)  # Extraindo o nome do arquivo

file_name = match_string.group(0)  # Pegando o nome do arquivo

path_file_name = path + f'\{file_name}'

df = pd.read_excel(path_file_name, sheet_name="ESTADOS", skiprows=9)  # Lendo o arquivo excel

df_filter = df.loc[df["PRODUTO"].str.contains("GASOLINA COMUM", case=False)]  # Filtrando o 'gasolina comum'

df_filter = df_filter[
    [
        "DATA INICIAL",
        "REGIAO",
        "ESTADOS",
        "NÚMERO DE POSTOS PESQUISADOS",
        "PREÇO MÉDIO REVENDA",
        "PREÇO MÍNIMO REVENDA",
        "PREÇO MÁXIMO REVENDA",
    ]
]  # Selecionando as colunas necessarias

df_filter.to_excel("resumo_semanal.xlsx", index=False)