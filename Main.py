import os
import csv
import requests
from bs4 import BeautifulSoup


def extract_url(page_url):
    request = requests.get(page_url)
    if request.ok:
        return request


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
    product_description = page_html.find('div', attrs={'id': 'product_description',
                                                       'class': 'sub-header'}).find_next('p').text
    category = page_html.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[2].contents[0]

    page_info = {'product_page_url': url_chosen, 'universal_ product_code (upc)': universal_product_code,
                 'title': title, 'price_including_tax': price_including_tax,'price_excluding_tax': price_excluding_tax,
                 'number_available': number_available, 'product_description': product_description, 'category':category,
                 'review_rating': review_rating, 'image_url': image_url}
    return  page_info


def create_csv(rows):
    header = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']

    with open('P2_01_extract.csv', 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, header)
        csv_writer.writeheader()
        csv_writer.writerow(rows)


def listing_url(url_site, book_category):
    url_category = url_site + 'catalogue/category/books/' + book_category + 'index.html'
    url_list = [url_site + 'catalogue/' + '/'.join(u.a['href'].split('/')[3:-1])
                for u in BeautifulSoup(extract_url(url_category).text, "html.parser").find_all('h3')]

    book_numbers = int(BeautifulSoup(extract_url(url_category).text, "html.parser")
                       .find('form', attrs={'class': 'form-horizontal'}).text[3:5])
    if book_numbers >= 20:
        if book_numbers % 20 == 0:
            for i in range(2, int(book_numbers//20)+1):
                url_category = url_site + 'catalogue/category/books/' + book_category + 'page-' + str(i) + '.html'
                url_list = url_list + [url_site + 'catalogue/' +
                                       '/'.join(u.a['href'].split('/')[3:-1])
                                       for u in BeautifulSoup(extract_url(url_category).text,
                                                              "html.parser").find_all('h3')]
        else:
            for i in range(2, int((book_numbers//20)+1)+1):
                url_category = url_site + 'catalogue/category/books/' + book_category + 'page-' + str(i) + '.html'
                url_list = url_list + [url_site + 'catalogue/' +
                                       '/'.join(u.a['href'].split('/')[3:-1])
                                       for u in BeautifulSoup(extract_url(url_category).text,
                                                              "html.parser").find_all('h3')]
    return url_list


#choix et requete de la page
url_site = 'http://books.toscrape.com/'
book_category = 'sequential-art_5/'
urls = listing_url(url_site, book_category)

#mise en forme des données
"""pages_data = transform_info(urls)"""
# liste de dictionnaires ou dictionnaire de listes?
# quid csv_writer?

"""
#creation du fichier CSV
create_csv(pages_data)

"""