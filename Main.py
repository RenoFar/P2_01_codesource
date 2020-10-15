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
    title = page_html.find('h1')

    tr_dic = {}
    for trs in page_html.findAll('tr'):
        ths = trs.findAll('th')
        tds = trs.findAll('td')
        tr_dic[ths[0].string] = tds[0].string

    universal_product_code = tr_dic['UPC']
    price_including_tax = tr_dic['Price (incl. tax)']
    price_excluding_tax = tr_dic['Price (excl. tax)']
    number_available = tr_dic['Availability']
    review_rating = tr_dic['Number of reviews']
   
    image_url = page_html.find('img')['src']

    product_description = page_html.find('div', attrs={'id':'product_description', 'class':'sub-header'}).find_next('p').text
    category = page_html.find('ul', attrs={'class':'breadcrumb'}).find_all('a')[2].contents[0]

    page_info = [product_page_url, universal_product_code, title.text, price_including_tax,
                 price_excluding_tax, number_available, product_description, category,
                 review_rating, image_url]


    """
   # Load
        # print(page_html.prettify())
    with open('P2_01_extract.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow('product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                             'price_excluding_tax', 'number_available', 'product_description', 'category',
                             'review_rating', 'image_url')
        # fonction add info in new line
    # csv_file.close()
    """