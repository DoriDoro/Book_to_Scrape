import csv
import requests
import re
import time

from urllib.parse import urljoin
from bs4 import BeautifulSoup as BfS

# the URL to scrape:
url = "http://books.toscrape.com/catalogue/category/books/history_32/index.html"
response = requests.get(url)

if response.ok:
    links = []
    soup = BfS(response.content, "html.parser")
    # find all <articles class="product_pod">:
    rows = soup.find_all("article")
    for row in rows:
        a = row.find("a")
        link = a["href"]
        # create link of each book:
        links.append("http://books.toscrape.com/catalogue/" + link)
    time.sleep(2)

# write the row data of the books for one category in csv-file:
# with open("category_data.csv", "w", newline="", encoding="utf-8") as file:
#     for link in links:
#         file.write(link.replace("../../../", "") + "\n")

# read data out of the csv-file:
with open("category_data.csv", "r", newline="", encoding="utf-8") as file:
    for row in file:
        url = row.strip()
        response = requests.get(url)
        if response.ok:
            soup = BfS(response.text, "html.parser")

            # search for information on website:
            # title
            title = soup.find("li", class_="active").string
            # universal product code (upc)
            upc = soup.find("th", text="UPC").find_next_sibling("td").string
            # price including tax (pit)
            pit = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
            # price_excluding_tax (pet)
            pet = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
            # available number
            available = soup.find("th", text="Availability").find_next_sibling("td").string
            # product description
            description = soup.find("div", id="product_description").find_next("p").string
            # category
            category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
            # review rating
            rating = soup.find("th", text="Number of reviews").find_next_sibling("td").string
            # image
            image = soup.find("img")
            image_url = image["src"]

# write information in csv-file:
with open("category.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Page URL:"])
    writer.writerow([url])

    writer.writerow(["Universal Product Code:"])
    writer.writerow([upc])

    writer.writerow(["Title:"])
    writer.writerow([title])

    writer.writerow(["Price including tax:"])
    writer.writerow([pit])

    writer.writerow(["Price excluding tax:"])
    writer.writerow([pet])

    writer.writerow(["Number available:"])
    writer.writerow([available.replace("In stock (", "").replace(")", "")])

    writer.writerow(["Product Description:"])
    writer.writerow([description])

    writer.writerow(["Category:"])
    writer.writerow([category])

    writer.writerow(["Review Rating:"])
    writer.writerow([rating])

    writer.writerow(["Image URL:"])
    writer.writerow([image_url])
