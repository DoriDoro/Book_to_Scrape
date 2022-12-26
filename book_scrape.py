# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import random
import re
import requests

from bs4 import BeautifulSoup as BfS


def get_url():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    if response.ok:
        links_of_categories = []
        soup = BfS(response.content, "html.parser")
        # take information for the sidebar: categories
        categories = soup.select(".side_categories a")
        for category in categories:
            link = category["href"]
            # create one link of each book:
            links_of_categories.append("http://books.toscrape.com/" + link)

        # choose a random category to scrape as URL:
        choose_one_category = random.choice(links_of_categories)
        response_single_book = requests.get(choose_one_category)
        soup_single_book = BfS(response_single_book.content, "html.parser")

        links_of_books = []
        # choose a random book on the page:
        # find all <article class="product_pod">:
        books = soup_single_book.find_all("article")
        for book in books:
            a = book.find("a")
            link = a["href"]  # link is string
            links_of_books.append("http://books.toscrape.com/catalogue/" + link.replace("../../../", ""))

        choose_one_book = random.choice(links_of_books)

    single_book(choose_one_book)


# create a function to scrape one book:
def single_book(choose_one_book):
    response = requests.get(choose_one_book)
    if response.ok:
        soup = BfS(response.content, "html.parser")
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
        rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
        # image
        image = soup.find("img")
        image_url = image["src"]

        # write information in csv-file:
        header = ["Product Page URL", "Universal Product Code", "Title", "Price including tax", "Price excluding tax",
                  "Number available", "Product Description", "Category", "Review Rating", "Image URL"]
        data = [choose_one_book, upc, title, pit, pet, available.replace("In stock (", "").replace(")", ""),
                description, category, rating, image_url.replace("../..", "http://books.toscrape.com")]

        with open(f"{category}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)


# create a function to scrape the categories:


# create a function for all books:
