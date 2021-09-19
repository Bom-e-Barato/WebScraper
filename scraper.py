import re
from time import process_time
import requests
import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Lists to store second hand names, prices and links of the products
sh_names = [] 
sh_prices = [] 
sh_links=[]    

# Lists to store first hand names, prices and links of the products
fh_names = [] 
fh_prices = [] 
fh_links=[]    


# OLX search function----------------------------------------------------------------------
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
                sh_names.append(product_name)
                sh_prices.append(product_price)
                sh_links.append(product_link)

                counter = counter + 1   # For deubgging purposes
                print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
            except:
                continue
    print(counter)  # For deubgging purposes


def cj_search(location, search_term):
    counter = 0
    page_num = 1
    while True:
        page = requests.get(f'https://www.custojusto.pt/{location}/q/{search_term}?o={page_num}&sp=1&st=a')
        soup = BeautifulSoup(page.text, 'lxml')
        products = soup.find_all('div', class_='container_related')

        if not products:
            break

        for product in products:
            # Get the data
            product_name = product.find('h2', class_='title_related').find('b').text
            product_price = float(product.find('h5', class_='price_related').text.strip()[:-2])
            product_link = product.find('a')['href']

            # Append the data to the lists
            sh_names.append(product_name)
            sh_prices.append(product_price)
            sh_links.append(product_link)

            counter = counter + 1   # For deubgging purposes
            page_num = page_num + 1
            print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')
    print(counter)


# FacebookMarketplace search function------------------------------------------------------Probabbly illegal, too bad
# def fb_search():
#     starting_url="https://www.facebook.com"
#     email="joaosilvascraper@gmail.com"
#     password="yJ-B'#YsEf.^G75H"

#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get("https://www.facebook.com/marketplace")
#     sleep(3)
    
#     driver.close
   

# KuantoKusta search function--------------------------------------------------------------
def kk_search(search_term):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    page = requests.get(f'https://www.kuantokusta.pt/search?q={search_term}&sort=3', headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')

    products = soup.find_all('div', class_='product-item-inner')
    
    for product in products:
        # Get the data
        product_name = product.find('a', class_='product-item-name')['title']
        product_price = product.find('a', class_='product-item-price').find('span').text[:-1].replace('.', '').replace(',', '.').strip()
        if 'Desde' in product_price:
            product_price = product_price[5:].strip()
        product_price = float(product_price)

        product_link = 'https://kuantokusta.pt/' + product.find('a', class_='product-item-store')['href']

        if product_link == 'https://kuantokusta.pt/#':
            encoded_link = product.find('a', class_='product-item-store')['onclick'].split(',')[2].replace('"', '').replace('\'', '').strip()
            product_link = urllib.parse.unquote(encoded_link)
        
        # Append the data to the lists
        fh_names.append(product_name)
        fh_prices.append(product_price)
        fh_links.append(product_link)

        print(f'Name: {product_name}\nPrice: {product_price}€\nLink: {product_link}\n')


def main():
    location_olx = 'ads'
    location_cj = 'portugal'
    search_term = input("Procurar: ").lower()               # Product name
    location_input = input('Regiao: ').lower()              # Region name
    if location_input != '':
        location_olx = location_input                       # Enter means the entier market

    olx_search_term = re.sub('\\s+', '-', search_term)      # Replace white spaces rows with '-'
    kk_search_term = re.sub('\\s+', '+', search_term)       # Replace white spaces rows with '+'
    cj_search_term = kk_search_term

    olx_search(location_olx, olx_search_term)               # Populate the list with OLX data
    cj_search(location_cj, cj_search_term)                  # Populate the list wtih CustoJusto data

    kk_search(kk_search_term)

    #fb_search()

    sh_d = {'nome': sh_names, 'precos': sh_prices, 'links': sh_links}
    pd.DataFrame(sh_d).sort_values('precos').to_json('sh_products.json', orient='index', indent=2, force_ascii=False)

    fh_d = {'nome': fh_names, 'precos': fh_prices, 'links': fh_links}
    pd.DataFrame(fh_d).sort_values('precos').to_json('fh_products.json', orient='index', indent=2, force_ascii=False)


if __name__ == '__main__':
    main()
