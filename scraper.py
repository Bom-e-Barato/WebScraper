import re
import requests
import pandas as pd
import urllib.parse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


names = []  # List to store the names of the products
prices = [] # List to store the prices of the products
links=[]    # List to store the links of the products




#OLX search function----------------------------------------------------------------------
def olx_search(location, search_term):
    counter = 0
    for i in range(25):
        page = requests.get(f'https://www.olx.pt/{location}/q-{search_term}/?page={i+1}')
        soup = BeautifulSoup(page.text, 'lxml')

        # Check if the request was redirected (happens when the page doesnt exist)
        if i != 0 and len(page.history) != 0 and page.history[0].url != '':
            break

        products = soup.find_all('div', class_ ='offer-wrapper')
        
        print()
        for product in products:
            try:
                # Get the data
                product_name = product.find('h3', class_='lheight22').find('strong').text
                product_price = float(product.find('p', class_='price').find('strong').text[:-2].replace('.', '').replace(',', '.'))
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



#KuantoKusta search function--------------------------------------------------------------
def kk_search(search_term):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    page = requests.get(f'https://www.kuantokusta.pt/search?q={search_term}&sort=3', headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')

    product = soup.find('div', class_='product-item-inner')

    product_name = product.find('a', class_='product-item-name')['title']
    product_price = product.find('a', class_='product-item-price').find('span').text[:-1].replace(',', '.')
    product_link = 'https://kuantokusta.pt/' + product.find('a', class_='product-item-store')['href']

    if product_link == 'https://kuantokusta.pt/#':
        encoded_link = product.find('a', class_='product-item-store')['onclick'].split(',')[2].strip().replace('"', '').replace('\'', '')
        product_link = urllib.parse.unquote(encoded_link)
    
    return {'nome': product_name, 'preco': product_price, 'link': product_link}



#FacebookMarketplace search function------------------------------------------------------Probabbly illegal, too bad
# def face_search():
#     starting_url="https://www.facebook.com"
#     email="joaosilvascraper@gmail.com"
#     password="yJ-B'#YsEf.^G75H"

#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get("https://www.facebook.com/marketplace")
#     sleep(3)
    
#     driver.close
    


def main():
    location_olx = 'ads'
    search_term = input("Procurar: ").lower()               # Product name
    location_input = input('Regiao: ').lower()              # Region name
    if location_input != '':
        location_olx = location_input                       # Enter means the entier market

    olx_search_term = re.sub('\\s+', '-', search_term)      # Replace white spaces rows with '-'
    kk_search_term = re.sub('\\s+', '+', search_term)       # Replace white spaces rows with '+'

    olx_search(location_olx, olx_search_term)               # Populate the list with OLX data
    print(kk_search(kk_search_term))

    #face_search()

    d = {'nome': names, 'precos': prices, 'links': links}
    pd.DataFrame(d).sort_values('precos').to_json('produtos.json', orient='index', indent=2, force_ascii=False)
    pd.DataFrame(kk_search(kk_search_term), index=[0]).to_json('best.json', orient='index', indent=2, force_ascii=False)

if __name__ == '__main__':
    main()
