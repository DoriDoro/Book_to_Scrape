# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import requests

from bs4 import BeautifulSoup as BfS

# function url
# function category
# function info
# function image plus write in csv
# function to read from csv


# the URL to scrape:
url = "http://books.toscrape.com/index.html"
response = requests.get(url)

if response.ok:
    soup = BfS(response.content, "html.parser")
    # search for <div class=side_categories> and select the <a> tag:
    categories = soup.select(".side_categories a")

    # create a list with all links of <a> tag:
    all_links = []
    for link_category in categories:
        # search for the href data:
        a = link_category["href"]
        # add link to list of links:
        all_links.append("http://books.toscrape.com/" + a)
        links = all_links[1:]
        # tells the links-list to start at the second link that is why we do not need to use replace
        # print(links) # for every category all links received

    # write information in csv-file:
    with open("books_data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
        for link in links:
            # print("link:", link)
            writer.writerow([link])

    # read information from csv-file:
    with open("books_data.csv", "r", newline="", encoding="utf-8") as file:
        for row in file:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BfS(response.text, "html.parser")

                # search for information on website:
                # title
                title = soup.find("li", class_="active").string
                # universal product code (upc)
                # a faire!!!!!
                # upc = soup.find("th", text="UPC").find_next_sibling("td").string
                # # price including tax (pit)
                # pit = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
                # # price_excluding_tax (pet)
                # pet = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
                # # available number
                available = soup.find("th", text="Availability").find_next_sibling("td").string
                # product description
                # description = soup.find("div", id="product_description").find_next("p").string
                # # category
                # category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
                # # review rating
                # rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
                # # image
                # image = soup.find("img")
                # image_url = image["src"]

# create for every category a csv file
# for book_cat in categories:
  # with open("{book_cat}.csv" ...)
with open("books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["All categories:"])
    for c in categories:
        category = c.text
        writer.writerow([category.replace("\n", "").replace(" ", "") + "\n"])

        writer.writerow(["Title:"])
        writer.writerow([title])
