import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


import csv

names = [] #List to store name of the product
prices = [] #List to store price of the product
links=[] #List to store link of the products



location_olx = 'ads'
search_term = input("Insira search term: ").lower() #inserir o search term na barra de pesquisa funciona, mas quebra a extração

location_input = input('Insira a regiao: ').lower()
if location_input != '':
    location_olx = location_input

re.sub('\\s+', '-', search_term) #sanatizar input de search

#apposto que o andré não apaga este comentário

olx_page = requests.get(f'https://www.olx.pt/{location_olx}/q-{search_term}').text
olx_soup = BeautifulSoup(olx_page,'lxml')

#print(soup.prettify())

##################################### OLX ##############################################
counter = 0
for i in range(25):
    page = requests.get(f'https://www.olx.pt/{location_olx}/q-{search_term}/?page={i+1}')
    soup = BeautifulSoup(page.text,'lxml')

    # Verificar se houve redirect do link (pagina não existir)
    if i != 0 and len(page.history) != 0 and page.history[0].url != '':
        break

    products = soup.find_all('div', class_ ='offer-wrapper')
    
    print()
    for product in products:
        try:
            product_name = product.find('h3', class_='lheight22').find('strong').text
        names.append(product_name)
        product_price = product.find('p', class_='price').find('strong').text[:-1]
        prices.append(product_price)
        product_link = product.find('a')['href']
        links.append(product_link)
        counter = counter + 1
        print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
        except:
            continue
print(counter)
########################################################################################


dict = {'Nome': names, 'precos': prices, 'links': links} #Criar cabeçalho do csv

df = pd.DataFrame(dict) # create dataframe from dictionary

df.to_json('Produtos.json', orient='index', indent=2)
