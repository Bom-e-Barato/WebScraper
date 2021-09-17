from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


driver=webdriver.Chrome(ChromeDriverManager().install()) #Create instance of chrome webDriver

# print("Insira search term") inserir o search term na barra de pesquisa funciona, mas quebra a extração
# search=input()

driver.get("https://www.olx.pt/")
Search = driver.find_element_by_id("headerSearch")



Search.send_keys("GTX 1050ti")
Search.send_keys(Keys.ENTER)


products=[] #List to store name of the product
prices=[] #List to store price of the product


content = driver.page_source
soup = BeautifulSoup(content,'lxml')


prices=soup.find_all('p',class_ ='price')
print(prices)








