import requests

from bs4 import BeautifulSoup as BfS

url = "http://books.toscrape.com/catalogue/category/books/history_32/index.html"
response = requests.get(url)

if response.ok:
    categories = []
    soup = BfS(response.text, "html.parser")
    rows = soup.findAll("ul", {"class": "nav"})
    for row in rows:
        inner_ul = row.findAll("ul")
        for ul in inner_ul:
            category = ul.findAll("a")
            categories.append(category)
    print(categories)
