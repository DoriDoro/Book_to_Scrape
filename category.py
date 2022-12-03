import requests
import re

from bs4 import BeautifulSoup as BfS

page = requests.get("http://books.toscrape.com/catalogue/category/books/history_32/index.html")
soup = BfS(page.content, "html.parser")

url_links = soup.find_all("div", class_="image_container")
for links in url_links:
    link_list = []
    link = links.find("a", href=True)
    link_list.append(link)
    print(link)



# title = soup.title.string
# upc = soup.find("th", text="UPC").find_next_sibling("td").string
# price_including_tax = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
# price_excluding_tax = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
# available = soup.find("p", class_="instock").text
# description = soup.find("div", id="product_description").find_next("p").string
# category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
# rating = soup.find("p", class_="star-rating Three")
# image = soup.find("img")
# image_url = image["src"]

with open("category.csv", "w") as csv_file:
    csv_file.write("Product Page URL: \n")
    csv_file.write(f"{link_list}\n\n")

    # csv_file.write("Universal Product Code: ")
    # csv_file.write(f"{upc}\n\n")
    #
    # csv_file.write("Title: ")
    # csv_file.write(f"{title}\n\n")
    #
    # csv_file.write("Price including tax: ")
    # csv_file.write(f"{price_including_tax}\n\n")
    #
    # csv_file.write("Price excluding tax: ")
    # csv_file.write(f"{price_excluding_tax}\n\n")
    #
    # csv_file.write("Number available: ")
    # csv_file.write(f"{available}\n\n")
    #
    # csv_file.write("Product Description: ")
    # csv_file.write(f"{description}\n\n")
    #
    # csv_file.write("Category: ")
    # csv_file.write(f"{category}\n\n")
    #
    # csv_file.write("Review Rating: ")
    # csv_file.write(f"{rating}\n\n")
    #
    # csv_file.write("Image URL: ")
    # csv_file.write(f"{image_url}\n\n")


