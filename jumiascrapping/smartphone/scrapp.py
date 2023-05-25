from pickle import NONE
from bs4 import BeautifulSoup 
import requests
from django.shortcuts import render
import csv
def extractSmartForCsv():
    with open('jumiaSmartphone.csv' ,'w',newline='\n' , encoding='utf-8') as file :
            writer = csv.writer(file)
            writer.writerow(['smartphoneName','smartphonePrice','smartphoneLink' , 'smartphoneImg','smartphoneBrand', 'smartphonePage',])
            
            for page in range(1, 15):
            #print('---', page, '---')
                url = 'https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page=' + str(page) + '#catalog-listing'
                r = requests.get(url)
                soup = BeautifulSoup(r.content, "html.parser")
                phone_class = soup.find_all("article", {"class": "prd _fb col c-prd"})
                
                for classes in phone_class:
                    link = classes.find("a" , {"class" : "core"})["href"]
                    phone_name = classes.find("h3", {"class": "name"}).text
                    phone_price = classes.find("div", {"class": "prc"}).text
                    phone_image = classes.find('div', {'class': 'img-c'}).find('img')['data-src']
                    phone_brand = classes.find("a", {"class" : "core"})["data-brand"]
                    writer.writerow([phone_name,phone_price,link,phone_image,phone_brand, page])
    print('done')

extractSmartForCsv()

def extractBrandsForCSv():
    with open('jumiaBrands.csv' ,'w',newline='\n' , encoding='utf-8') as file :
            writer = csv.writer(file)
            writer.writerow(['Brand'])
            url = "https://www.jumia.com.tn/smartphones/";            
            page = requests.get(url)
            src = page.content
            soup = BeautifulSoup(src, 'lxml')

            brands_element = soup.find("div" , {"class" : "-phs -pvxs -df -d-co -h-168 -oya -sc"})
            for i in range(len(brands_element)):
                writer.writerow([brands_element.contents[i].text])
    print('done')
#extractBrandsForCSv()