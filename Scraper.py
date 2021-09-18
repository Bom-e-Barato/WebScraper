import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

location_olx = 'ads'
search_term = input("Insira search term: ") #inserir o search term na barra de pesquisa funciona, mas quebra a extração

location_input = input('Insira a regiao: ')
if location_input != '':
    location_olx = location_input.lower()

search_term.replace(' ', '-').lower()

products = [] #List to store name of the product
prices = [] #List to store price of the product

olx_page = requests.get(f'https://www.olx.pt/{location_olx}/q-{search_term}').text
olx_soup = BeautifulSoup(olx_page,'lxml')

#print(soup.prettify())

products = olx_soup.find_all('div', class_ ='offer-wrapper')

print()
for product in products:
    product_name = product.find('h3', class_='lheight22').find('strong').text
    product_price = product.find('p', class_='price').find('strong').text[:-1]
    product_link = product.find('a')['href']
    print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
