import requests
import re

from bs4 import BeautifulSoup as BfS

url = "http://books.toscrape.com/catalogue/the-murder-that-never-was-forensic-instincts-5_939/index.html"
page = requests.get(url)
soup = BfS(page.content, "html.parser")

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

with open("single_book.csv", "w") as csv_file:
    csv_file.write("Product Page URL:\n")
    csv_file.write(url + "\n\n")

    csv_file.write("Universal Product Code:\n")
    csv_file.write(upc + "\n\n")

    csv_file.write("Title:\n")
    csv_file.write(title.replace("\n", "") + "\n\n")

    csv_file.write("Price including tax:\n")
    csv_file.write(pit + "\n\n")

    csv_file.write("Price excluding tax:\n")
    csv_file.write(pet + "\n\n")

    csv_file.write("Number available:\n")
    csv_file.write(available + "\n\n")

    csv_file.write("Product Description:\n")
    csv_file.write(description + "\n\n")

    csv_file.write("Category:\n")
    csv_file.write(category + "\n\n")

    csv_file.write("Review Rating:\n")
    csv_file.write(str(rating) + "\n\n")

    csv_file.write("Image URL:\n")
    csv_file.write(image_url)


