import requests

from bs4 import BeautifulSoup as BfS

url = "http://books.toscrape.com/index.html"
response = requests.get(url)

if response.ok:
    categories = []
    soup = BfS(response.text, "html.parser")
    rows = soup.find_all("ul", {"class": "nav"})
    for row in rows:
        inner_ul = row.find_all("ul")
        for ul in inner_ul:
            category = ul.find_all("a")
            categories.append(category)
    print(categories)
