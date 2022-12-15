import csv
import requests
import re

from bs4 import BeautifulSoup as BfS

# the URL to scrape:
url = "http://books.toscrape.com/catalogue/the-murder-that-never-was-forensic-instincts-5_939/index.html"
page = requests.get(url)
soup = BfS(page.content, "html.parser")

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
with open("single_book.csv", "w", newline="", encoding="utf-8") as file:
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


