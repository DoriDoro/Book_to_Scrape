import requests
import re
import time

from bs4 import BeautifulSoup as BfS

url = "http://books.toscrape.com/catalogue/category/books/history_32/index.html"
response = requests.get(url)

if response.ok:
    links = []
    soup = BfS(response.text, "html.parser")
    rows = soup.find_all("article")
    for row in rows:
        a = row.find("a")
        link = a["href"]
        links.append("http://books.toscrape.com/catalogue/" + link)
    time.sleep(3)

# with open("category_data.csv", "w", encoding="utf-8") as file:
#     for link in links:
#         file.write(link.replace("../../../", "") + "\n")

with open("category_data.csv", "r", encoding="utf-8") as file:
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

with open("category.csv", "w", encoding="utf-8") as csv_file:
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
    csv_file.write(available.replace("In stock (", "").replace(")", "") + "\n\n")

    csv_file.write("Product Description:\n")
    csv_file.write(description + "\n\n")

    csv_file.write("Category:\n")
    csv_file.write(category + "\n\n")

    csv_file.write("Review Rating:\n")
    csv_file.write(rating + "\n\n")

    csv_file.write("Image URL:\n")
    csv_file.write(image_url)

