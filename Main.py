import os
import csv
import requests
from bs4 import BeautifulSoup

request = requests.get("https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html")
page = request.content
soup = BeautifulSoup(request.text, "html.parser")