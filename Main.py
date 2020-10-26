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

    if page_html.find('article', 'product_page').find('p', recursive = False) is not None:
        product_description = page_html.find('article', 'product_page').find('p', recursive=False).text
    else:
        product_description = ""

    category = page_html.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[2].contents[0]

    page_info = [url_chosen, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
                 product_description, category, review_rating, image_url]
    """print(page_info)"""
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


def listing_url(url_site, book_cat):
    url_category = url_site + 'catalogue/category/books/' + book_cat + '/index.html'
    print(url_category)
    url_list = [url_site + 'catalogue/' + '/'.join(u.a['href'].split('/')[3:-1])
                for u in BeautifulSoup(extract_url(url_category).text, "html.parser").find_all('h3')]

    book_numbers = int(BeautifulSoup(extract_url(url_category)
                                     .text, "html.parser").find('form', attrs={'class': 'form-horizontal'})
                       .text.split('\n')[3].split(' ')[0])
    """print(book_numbers)"""
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


def writing_data(url_lists, books_cat):
    counter = 0
    pages_data = []
    for u in range(len(url_lists)):
        pages_data.append(transform_info(url_lists[u]))
        counter += 1
    """print(pages_data)"""
    create_csv(pages_data, books_cat)
    """print(str(counter))"""
    return counter

def listing_category(home_page):
    category_list = [home_page + u.a['href']
                for u in BeautifulSoup(extract_url(home_page).text, "html.parser")
                         .find('ul', attrs={'class': 'nav nav-list'}).find_all('li')]
    return category_list


"""transform_info('http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html')"""

#choix et requete des pages
url_site = 'http://books.toscrape.com/'
list_cat = listing_category(url_site)

#mise en forme et écriture des données
book_category = []
count = 0
for c in range(1,len(list_cat)):
    book_category = list_cat[c].split('/')[-2:-1]
    urls_list = listing_url(url_site, book_category[0])
    print(urls_list)
    count += writing_data(urls_list, book_category[0])

#total de scraping réussis
print(str(count))
