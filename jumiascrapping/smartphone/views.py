from bs4 import BeautifulSoup
import requests
from django.shortcuts import render
import csv

def extractPhones(request, pagination=1):
    page = pagination
    filtered_phones = []
    with open('jumiaSmartphone.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignore the first line (header)
        
        for row in reader:
            if (page == int(row[5])):
                phone_name = row[0]
                phone_price = float(row[1].replace(' TND', '').replace(',', ''))  # Convert the price to a float
                phone_brand = row[4]
                phone_link = row[2]
                phone_image = row[3]
                filtered_phones.append({
                'smartphoneName': phone_name,
                'smartphonePrice': phone_price,
                'smartphoneLink': phone_link,
                'smartphoneImg': phone_image,
                'smartphoneBrand': phone_brand
            })
                
    brands = extractBrands()
    context = {'data': filtered_phones, 'brands': brands, 'pagination': range(1, 15)}
    return render(request, 'first.html', context)

def extractBrands():
    url = "https://www.jumia.com.tn/smartphones/"
    brands = []
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, 'lxml')

    brands_element = soup.find("div", {"class": "-phs -pvxs -df -d-co -h-168 -oya -sc"})
    for i in range(len(brands_element.contents)):
        brands.append(brands_element.contents[i].text)
    return brands

def filtrageBybrands(selectedBrand):
    filtered_phones = []

    with open('jumiaSmartphone.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignorer l'en-tête du fichier CSV

        for row in reader:
            phone_name = row[0]
            phone_price = row[1]
            phone_link = row[2]
            phone_image = row[3]
            phone_brand = row[4]

            # Filtrer les téléphones en fonction de la marque sélectionnée
            marque = phone_brand
            if marque in selectedBrand:
                filtered_phones.append({
                    'smartphoneName': phone_name,
                    'smartphonePrice': phone_price,
                    'smartphoneLink': phone_link,
                    'smartphoneImg': phone_image,
                    'smartphoneBrand': phone_brand
                })
    return filtered_phones

def filtrageByPrix(prixMin, prixMax):
    filtered_phones = []
    with open('jumiaSmartphone.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignorer l'en-tête du fichier CSV

        for row in reader:
            phone_name = row[0]
            phone_price_str = row[1].replace('TND', '').replace(',', '')  # Supprimer 'DT' et les virgules
            phone_price = float(phone_price_str)  # Convertir le prix en nombre flottant
            phone_link = row[2]
            phone_image = row[3]
            phone_brand = row[4]

            # Filtrer les téléphones en fonction du prix minimum et maximum
            if prixMin <= phone_price <= prixMax:
                phone_data = {
                    'smartphoneName': phone_name,
                    'smartphonePrice': phone_price,
                    'smartphoneLink': phone_link,
                    'smartphoneImg': phone_image,
                    'smartphoneBrand': phone_brand
                }
                filtered_phones.append(phone_data)

    return filtered_phones

def filtrageByPrixAndBrand(min_price, max_price, selected_brands):
    filtered_phones = []
    with open('jumiaSmartphone.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignore the first line (header)
        for row in reader:
            phone_name = row[0]
            phone_price = float(row[1].replace(' TND', '').replace(',', ''))  # Convert the price to a float
            phone_brand = row[4]
            phone_link = row[2]
            phone_image = row[3]
            if min_price <= phone_price <= max_price and phone_brand in selected_brands:
                phone_data = {
                    'smartphoneName': phone_name,
                    'smartphonePrice': phone_price,
                    'smartphoneBrand': phone_brand,
                    'smartphoneLink': phone_link,
                    'smartphoneImg': phone_image,
                }
                filtered_phones.append(phone_data)
    
    return filtered_phones

def get_all_phones():
    filtered_phones = []
    with open('jumiaSmartphone.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Ignore the first line (header)
        for row in reader:
            phone_name = row[0]
            phone_price = float(row[1].replace(' TND', '').replace(',', ''))  # Convert the price to a float
            phone_brand = row[4]
            phone_link = row[2]
            phone_image = row[3]
            phone_data = {
                'smartphoneName': phone_name,
                'smartphonePrice': phone_price,
                'smartphoneBrand': phone_brand,
                'smartphoneLink': phone_link,
                'smartphoneImg': phone_image,
            }
            filtered_phones.append(phone_data)
    return filtered_phones

def filterPhones(request):
    filtered_phones = []
    selected_brands = request.POST.getlist('brands')
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')
    
    if not selected_brands and not min_price and not max_price:
        filtered_phones = get_all_phones()
    else: 
        if selected_brands and not min_price and not max_price:
            filtered_phones = filtrageBybrands(selected_brands)
        elif not selected_brands and min_price and max_price:
            filtered_phones = filtrageByPrix(float(min_price), float(max_price))
        elif selected_brands and min_price and max_price:
            filtered_phones = filtrageByPrixAndBrand(float(min_price), float(max_price), selected_brands)
    
    context = {'filtered_phones': filtered_phones, 'selected_brands': selected_brands}
    return render(request, 'search.html', context)
