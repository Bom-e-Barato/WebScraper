import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

location_olx = 'ads'
search_term = input("Insira search term: ").lower() #inserir o search term na barra de pesquisa funciona, mas quebra a extração

location_input = input('Insira a regiao: ').lower()
if location_input != '':
    location_olx = location_input

re.sub('\\s+', '-', search_term)


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
        product_name = product.find('h3', class_='lheight22').find('strong').text
        product_price = product.find('p', class_='price').find('strong').text[:-1]
        product_link = product.find('a')['href']
        counter = counter + 1
        print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
    print(counter)
########################################################################################

