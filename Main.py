import os
import csv
import requests
from bs4 import BeautifulSoup

# Extract
page_selection = requests.get("http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html")

# Transform
page_html = BeautifulSoup(page_selection.text, "html.parser")

product_page_url = []
for page_url in page_html.find_all('a'):
    product_page_url.append(page_url.get('href'))


# Load
""" print(page_html.prettify())"""
print(product_page_url)