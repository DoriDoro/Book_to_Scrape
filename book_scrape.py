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
        links_of_categories_all = []
        soup = BfS(response.content, "html.parser")
        # take information for the sidebar: categories
        categories = soup.select(".side_categories a")
        for category in categories:
            link = category["href"]
            # create one link of each book:
            links_of_categories_all.append(f"http://books.toscrape.com/{link}")
            # start from the second link:
            links_of_categories = links_of_categories_all[1:]

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
            links_of_books.append(f'http://books.toscrape.com/catalogue/{link.replace("../../../", "")}')

        choose_one_book = random.choice(links_of_books)

    single_book(choose_one_book)
    category_scrape(random.choice(links_of_categories))
    all_books(links_of_categories)


# scrape one book:
def single_book(choose_one_book):
    data = [choose_one_book]
    response = requests.get(choose_one_book)
    if response.ok:
        soup = BfS(response.content, "html.parser")
        # search for information on website:
        # title
        title = soup.find("li", class_="active").string
        data.append(title)
        # universal product code (upc)
        upc = soup.find("th", text="UPC").find_next_sibling("td").string
        data.append(upc)
        # price including tax (pit)
        pit = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
        data.append(pit)
        # price_excluding_tax (pet)
        pet = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
        data.append(pet)
        # available number
        available = soup.find("th", text="Availability").find_next_sibling("td").string
        data.append(available.replace("In stock (", "").replace(")", ""))
        # product description
        description = soup.find("div", id="product_description").find_next("p").string
        data.append(description)
        # category
        category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
        data.append(category)
        # review rating
        rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
        data.append(rating)
        # image
        image = soup.find("img")
        image_url = image["src"]
        data.append(image_url.replace("../..", "http://books.toscrape.com"))

        write_csv(data)


def write_csv(data):
    # write information in csv-file:
    header = ["Product Page URL", "Universal Product Code", "Title", "Price including tax", "Price excluding tax",
              "Number available", "Product Description", "Category", "Review Rating", "Image URL"]
    lines = [data]

    with open(f"{data[7]}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(lines)


# scrape the categories:
def category_scrape(choose_one_category):
    print("------ choose ", choose_one_category)
    response = requests.get(choose_one_category)
    if response.ok:
        links = []
        soup = BfS(response.content, "html.parser")
        # find all <article class="product_pod">:
        articles = soup.find_all("article")
        for article in articles:
            a = article.find("a")
            a_link = a["href"]
            # create link of each book:
            links.append(f'http://books.toscrape.com/catalogue/{a_link.replace("../../../", "")}')

        write_csv_link(links)

        # read row data from file and get information:
        with open("row_data.csv", "r", newline="", encoding="utf-8") as file:
            for row in file:
                url = row.strip()
                single_book(url)
                print("- - - ", url)
                # writes just the last one in csv file instead of all


# write links as row data in csv file:
def write_csv_link(links):
    with open("row_data.csv", "w", newline="", encoding="utf-8") as file:
        for link in links:
            writer = csv.writer(file)
            writer.writerow([link])


# scrape all books:
def all_books(links_of_categories):
    category_links = []
    for link in links_of_categories:
        response = requests.get(link)
        category_links.append(link)
    if response.ok:
        write_csv_link(category_links)
        print(category_links)
        for one_category in category_links:
            print("--------------------", one_category)
            category_scrape(one_category)


get_url()
