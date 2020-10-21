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


def create_csv(rows, name_cat):
    header = list(rows.keys())

    with open('P2_01_' + str(name_cat) + '.csv', 'a', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, header)
        if os.stat('P2_01_' + str(name_cat) + '.csv').st_size == 0:
            csv_writer.writeheader()
        csv_writer.writerow(rows)


def listing_url(url_site, book_cat):
    url_category = url_site + 'catalogue/category/books/' + book_cat + '/index.html'
    url_list = [url_site + 'catalogue/' + '/'.join(u.a['href'].split('/')[3:-1])
                for u in BeautifulSoup(extract_url(url_category).text, "html.parser").find_all('h3')]

    book_numbers = int(BeautifulSoup(extract_url(url_category).text, "html.parser")
                       .find('form', attrs={'class': 'form-horizontal'}).text[3:5])
    if book_numbers >= 20:
        if book_numbers % 20 == 0:
            for i in range(2, int(book_numbers//20)+1):
                url_category = url_site + 'catalogue/category/books/' + book_cat + '/page-' + str(i) + '.html'
                url_list = url_list + [url_site + 'catalogue/' +
                                       '/'.join(u.a['href'].split('/')[3:-1])
                                       for u in BeautifulSoup(extract_url(url_category).text,
                                                              "html.parser").find_all('h3')]
        else:
            for i in range(2, int((book_numbers//20)+1)+1):
                url_category = url_site + 'catalogue/category/books/' + book_cat + '/page-' + str(i) + '.html'
                url_list = url_list + [url_site + 'catalogue/' +
                                       '/'.join(u.a['href'].split('/')[3:-1])
                                       for u in BeautifulSoup(extract_url(url_category).text,
                                                              "html.parser").find_all('h3')]
    return url_list

#def listing_category():

def Writing_data(url_lists, books_cat):
    for u in range(len(url_lists)):
        pages_data = urls[u]
        """pages_data = transform_info(url_lists[u])"""
        create_csv(pages_data, books_cat)


#choix et requete des pages
url_site = 'http://books.toscrape.com/'
book_category = 'sequential-art_5'

"""urls = listing_url(url_site, book_category)"""
urls =({'product_page_url': '1', 'universal_ product_code (upc)': '2',
        'title': '3', 'price_including_tax': '4','price_excluding_tax': '5',
        'number_available': '6', 'product_description': '7', 'category':'8',
        'review_rating': '9', 'image_url': '10'},
       {'product_page_url': '11', 'universal_ product_code (upc)': '12',
        'title': '13', 'price_including_tax': '14', 'price_excluding_tax': '15',
        'number_available': '16', 'product_description': '17', 'category': '18',
        'review_rating': '19', 'image_url': '20'},
       {'product_page_url': '21', 'universal_ product_code (upc)': '2',
        'title': '23', 'price_including_tax': '24', 'price_excluding_tax': '25',
        'number_available': '26', 'product_description': '27', 'category': '28',
        'review_rating': '29', 'image_url': '30'},
       {'product_page_url': '31', 'universal_ product_code (upc)': '32',
        'title': '33', 'price_including_tax': '34', 'price_excluding_tax': '35',
        'number_available': '36', 'product_description': '37', 'category': '38',
        'review_rating': '39', 'image_url': '40'})
#mise en forme et écriture des données
Writing_data(urls, book_category)
