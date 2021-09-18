import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


names = []  # List to store the names of the products
prices = [] # List to store the prices of the products
links=[]    # List to store the links of the products

def olx_search():
    counter = 0
    for i in range(25):
        page = requests.get(f'https://www.olx.pt/{location_olx}/q-{search_term}/?page={i+1}')
        soup = BeautifulSoup(page.text,'lxml')

        # Check if the request was redirected (happens when the page doesnt exist)
        if i != 0 and len(page.history) != 0 and page.history[0].url != '':
            break

        products = soup.find_all('div', class_ ='offer-wrapper')
        
        print()
        for product in products:
            try:
                # Get the data
                product_name = product.find('h3', class_='lheight22').find('strong').text
                product_price = product.find('p', class_='price').find('strong').text[:-1]
                product_link = product.find('a')['href']
                
                # Append the data to the lists
                names.append(product_name)
                prices.append(product_price)
                links.append(product_link)

                counter = counter + 1   # For deubgging purposes
                print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
            except:
                continue
    print(counter)  # For deubgging purposes

location_olx = 'ads'
search_term = input("Procurar: ").lower()   # Product name
location_input = input('Regiao: ').lower()  # Region name
if location_input != '':
    location_olx = location_input           # Enter means the entier market

re.sub('\\s+', '-', search_term)            # Replace white spaces rows with '-'

olx_search()

dict = {'Nome': names, 'precos': prices, 'links': links}
df = pd.DataFrame(dict)                     # Create the Dataframe from the dictionary
df.to_json('Produtos.json', orient='index', indent=2)
