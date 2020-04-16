import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome(os.getenv("PATH_CHROMEDRIVER"))
print("We've just started scraping street icecream australia")
driver.get("https://www.streetsicecream.com.au/home.html")
content = driver.page_source
soup = BeautifulSoup(content,features="html.parser")
dfs = []
writer = pd.ExcelWriter('street.xlsx', engine='openpyxl')
print("Here we gooooo:")
for a in soup.findAll('div', attrs={'class':'c-featured-content-image col-sm-6'}):
    myhref = a.find('a', attrs={'class':"c-featured-content-image__link"}).get('href')
    print(myhref)
    driver.get(myhref)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    for a in soup.findAll('div', attrs={'class':'c-product-listing-v2-item clearfix'}):
        myhref = a.find('a', attrs={'class':"c-product-listing-v2-item-image__link"}).get('href')
        name = a.find('a', attrs={'data-ct-action':'productClick'}).get('title')
        driver.get(myhref)
        content = driver.page_source
        soup = BeautifulSoup(content,features="html.parser")
        for a in soup.findAll('div', attrs={'class':'c-product-nutrients__info-item__ni'}):
            headers = [text.text.strip() for text in a.find_all('th', attrs={'scope':'col'})]
            ni0 = [text.text.strip() for text in a.find_all('th', attrs={'class':'ni-facts-0','scope':'row'})]
            ni1 = [text.text.strip() for text in a.find_all('td',attrs={'class':'ni-facts-1'})]
            ni2 = [text.text.strip() for text in a.find_all('td',attrs={'class':'ni-facts-2'})]
            ni3 = [text.text.strip() for text in a.find_all('td',attrs={'class':'ni-facts-3'})]
            df = pd.DataFrame({headers[0]:ni0,headers[1]:ni1,headers[2]:ni2,headers[3]:ni3}) 
            df.to_excel(writer, name, index=False)
print("Writing to excel file")
writer.save()
print("We're done! Horraay!")