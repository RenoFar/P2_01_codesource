#Importation des modules
import os
import csv
import requests
from bs4 import BeautifulSoup

#Définitions des fonctions
def extract_url(page_url):  #Test de présence de l'url et récupération des données
    request = requests.get(page_url)
    if request.ok:
        return request

def listing_category(home_page): #Extraction et mise en forme de la  liste des catégories
    category_list = [home_page + u.a['href']
                for u in BeautifulSoup(extract_url(home_page).text, "html.parser")
                         .find('ul', attrs={'class': 'nav nav-list'}).find_all('li')]
    return category_list

def listing_url(url_site, book_cat): #Création de la liste des urls par catégorie
    #Mise en forme de l'url à extraire
    book_cat = book_cat.split('/')[-2:-1][0]
    print('\nCatégorie: ' + book_cat)
    url_category = url_site + 'catalogue/category/books/' + book_cat + '/index.html'
    print(url_category)

    #Récupération des urls de la première page
    url_list = [url_site + 'catalogue/' + '/'.join(u.a['href'].split('/')[3:-1])
                for u in BeautifulSoup(extract_url(url_category).text, "html.parser").find_all('h3')]

    #Détermination du nombre de livre dans la catégorie
    book_numbers = int(BeautifulSoup(extract_url(url_category)
                                     .text, "html.parser").find('form', attrs={'class': 'form-horizontal'})
                       .text.split('\n')[3].split(' ')[0])
    page_numbers = 1
    print('nombre de livre: ' + str(book_numbers))

    #Récupération des urls sur les pages suivantes si elles existent
    if book_numbers >= 20:
        #Détermination du nombre de page d'url à extraire: 20 par page
        if book_numbers % 20 == 0:
            page_numbers = book_numbers//20
        else:
            page_numbers = book_numbers // 20 + 1
        #Rajout des urls des pages suivantes à la liste
        for i in range(2, int(page_numbers + 1)):
            url_category = url_site + 'catalogue/category/books/' + book_cat + '/page-' + str(i) + '.html'
            url_list = url_list + [url_site + 'catalogue/' +'/'.join(u.a['href'].split('/')[3:-1])
                                   for u in BeautifulSoup(extract_url(url_category).text, "html.parser").find_all('h3')]
    print('nombre de page: ' + str(page_numbers))
    return url_list

def transform_info(url_chosen):
    page_html = BeautifulSoup(extract_url(url_chosen).text, "html.parser")

    title = page_html.find('h1').text

    tr_dic = {}
    for trs in page_html.findAll('tr'):
        ths = trs.findAll('th')
        tds = trs.findAll('td')
        tr_dic[ths[0].string] = tds[0].string

    universal_product_code = tr_dic['UPC']
    price_including_tax = tr_dic['Price (incl. tax)'][1:]
    price_excluding_tax = tr_dic['Price (excl. tax)'][1:]
    number_available = tr_dic['Availability']
    review_rating = tr_dic['Number of reviews']

    image_url = url_site + '/'.join(page_html.find('img')['src'].split('/')[2:])

    if page_html.find('article', 'product_page').find('p', recursive = False) is not None:
        product_description = page_html.find('article', 'product_page').find('p', recursive=False).text
    else:
        product_description = ""

    category = page_html.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[2].contents[0]

    page_info = [url_chosen, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                 product_description, category, review_rating, image_url]
    return  page_info

def create_csv(rows, name_cat):
    header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']
    with open('P2_01_' + str(name_cat) + '.csv', 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if os.stat('P2_01_' + str(name_cat) + '.csv').st_size == 0:
            csv_writer.writerow(header)
        for r in range(len(rows)):
            csv_writer.writerow(rows[r])

def writing_data(url_lists, books_cat):
    counter = 0
    pages_data = []
    for u in range(len(url_lists)):
        pages_data.append(transform_info(url_lists[u]))
        counter += 1
    create_csv(pages_data, books_cat)
    return counter


#Choix et requete des pages
url_site = 'http://books.toscrape.com/' #Selection de l'url de la page principale du site
list_cat = listing_category(url_site) #Récupération de la liste des catégories

#Mise en forme et écriture des données
count = 0 #Initialisation du compteur de nombre d'urls traités

for c in range(1,len(list_cat)): #Boucle de traitement par catégorie
    #Récupération de la liste des urls par catégorie
    urls_list = listing_url(url_site, list_cat[c])
    #Suivi des urls récupérées
    print(urls_list)
    print('nombre d'' url(s) récupérée(s): ' + str(len(urls_list)))
    """count += writing_data(urls_list, list_cat[c])"""

#Total de scraping réussis
print('nombre total d''urls traitées ' + str(count))
