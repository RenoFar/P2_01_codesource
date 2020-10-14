import os
import csv
import requests
from bs4 import BeautifulSoup

# Extract
request = requests.get("http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html")
page_selection = request.text

# Transform
page_html = BeautifulSoup(page_selection, "html.parser")
""" product_page_url = []
for page_url in page_html.find_all('a'):
    product_page_url.append(page_url.get('href'))"""

# Load
""" print(page_html.prettify())"""
with open('P2_01_extract.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['product_page_url', request.url])
csv_file.close()
