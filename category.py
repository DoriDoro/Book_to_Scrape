import requests
import re
import time

from bs4 import BeautifulSoup as BfS

url = "http://books.toscrape.com/catalogue/category/books/history_32/index.html"
response = requests.get(url)

if response.ok:
    links = []
    soup = BfS(response.text, "html.parser")
    rows = soup.findAll("article")
    for row in rows:
        a = row.find("a")
        link = a["href"]
        links.append("http://books.toscrape.com/catalogue/" + link)
    time.sleep(3)

# with open("category.csv", "w") as file: or txt file
#     for link in links:
#         file.write(link.replace("../../../", "") + "\n")

with open("category.csv", "r") as file:
    for row in file:
        url = row.strip()
        response = requests.get(url)
        if response.ok:
            soup = BfS(response.text, "html.parser")

            # title
            title = soup.title.string
            # universal product code (upc)
            upc = soup.find("th", text="UPC").find_next_sibling("td").string
            # price including tax (pit)
            pit = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
            # price_excluding_tax (pet)
            pet = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
            # available number
            available = soup.find("p", class_="instock").text
            # product description
            description = soup.find("div", id="product_description").find_next("p").string
            # category
            category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
            # review rating
            rating = soup.find("p", class_="star-rating Three")
            # image
            image = soup.find("img")
            image_url = image["src"]
