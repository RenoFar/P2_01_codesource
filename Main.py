import os
import csv
import requests
from bs4 import BeautifulSoup

# Extract
url = "http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html"
request = requests.get(url)
if request.ok:

    # Transform
    page_html = BeautifulSoup(request.text, "html.parser")

    product_page_url = url
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
   
    image_url = 'http://books.toscrape.com/' + '/'.join(page_html.find('img')['src'].split('/')[2:])

    product_description = page_html.find('div', attrs={'id':'product_description', 'class':'sub-header'}).find_next('p').text
    category = page_html.find('ul', attrs={'class':'breadcrumb'}).find_all('a')[2].contents[0]

    page_info = [product_page_url, universal_product_code, title, price_including_tax,
                 price_excluding_tax, number_available, product_description, category,
                 review_rating, image_url]

    # Load
    with open('P2_01_extract.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        Header = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                 'price_excluding_tax', 'number_available', 'product_description', 'category',
                 'review_rating', 'image_url']
        csv_writer.writerow(Header)
        csv_writer.writerow(page_info)
    # csv_file.close()
