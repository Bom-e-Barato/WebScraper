from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


search_term = input("Insira search term: ") #inserir o search term na barra de pesquisa funciona, mas quebra a extração

driver = webdriver.Chrome(ChromeDriverManager().install()) #Create instance of chrome webDriver
driver.get("https://www.olx.pt/")
Search = driver.find_element_by_id("headerSearch")

Search.send_keys(search_term)
Search.send_keys(Keys.ENTER)

products = [] #List to store name of the product
prices = [] #List to store price of the product

content = driver.page_source
soup = BeautifulSoup(content,'lxml')

products = soup.find_all('div', class_ ='offer-wrapper')

print()
for product in products:
    product_name = product.find('h3', class_='lheight22').find('strong').text
    product_price = product.find('p', class_='price').find('strong').text[:-1]
    product_link = product.find('a')['href']
    print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
