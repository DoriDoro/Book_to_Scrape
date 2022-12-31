# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import random
import re
import requests

from bs4 import BeautifulSoup as BfS


# issues: some titles (sports-and-games or poetry) was not .csv
# http://books.toscrape.com/catalogue/category/books/fiction_10/page-3.html for each category


def get_url():
    print("--------------------start--------------------")
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

        get_category_links(links_of_categories)

    category = ["Travel", "Mystery", "Historical Fiction", "Sequential Art", "Classics", "Philosophy", "Romance",
                "Womens Fiction", "Fiction", "Childrens", "Religion", "Nonfiction", "Music", " Default",
                "Science Fiction", "Sports and Games", "Add a comment", "Fantasy", "New Adult", "Young Adult",
                "Science", "Poetry", "Paranormal", "Art", "Psychology", "Autobiography", "Parenting", "Adult Fiction",
                "Humor", "Horror", "History", "Food and Drink", "Christian Fiction", "Business", "Biography",
                "Thriller", "Contemporary", "Spirituality", "Academic", "Self Help", "Historical", "Christian",
                "Suspense", "Short Stories", "Novels", "Health", "Politics", "Cultural", "Erotica", "Crime"]

    # scrap_the_whole_site()
    category_scrape(random.choice(category))
    # single_book(book)


def get_category_links(links_of_categories):
    # create list for all category links:
    category_links = []
    for link in links_of_categories:
        response = requests.get(link)
        if response.ok:
            category_links.append(link)
            # write all category links in a csv file:
            write_csv_link(category_links, name="category_links")


# scrape all books:
def scrap_the_whole_site():
    print("----------start all----------")
    # read information from csv-file to get the category links:
    with open("results/category_links.csv", "r", newline="", encoding="utf-8") as file:
        for link in file:
            url = link.strip()
            # # create a variable to get the category as name for the csv file:
            # category = url.replace("http://books.toscrape.com/catalogue/category/books/", "").replace("/index.html", "")
            # category = re.sub(r"\_[0-9]|[0-9]", "", category)
            response = requests.get(url)
            if response.ok:
                book_in_category = []
                soup = BfS(response.content, "html.parser")
                # find all <article class="product_pod">:
                articles = soup.find_all("article")
                for article in articles:
                    a = article.find("a")
                    a_link = a["href"]
                    # create link of each book:
                    book_in_category.append(f'http://books.toscrape.com/catalogue/{a_link.replace("../../../", "")}')
                # write all books from each category in csv file:
                # append_csv_link(book_in_category, name=f"books_in_cat_{category}")


# write links as row data in csv file:
def write_csv_link(links, name):
    with open(f"results/{name}.csv", "w", newline="", encoding="utf-8") as file:
        for link in links:
            writer = csv.writer(file)
            writer.writerow([link])


# append links as row data in csv file:
def append_csv_link(links, name):
    with open(f"results/{name}.csv", "a", newline="", encoding="utf-8") as file:
        for link in links:
            writer = csv.writer(file)
            writer.writerow([link])


# scrape the categories:
# enter a category
def category_scrape(category):
    print("----------start category----------")
    category_lower = category.lower()
    final_category = category_lower.replace(" ", "-")

    # read information from csv-file to get the link of one book of one category:
    with open(f"results/books_in_cat_{final_category}.csv", "r", newline="", encoding="utf-8") as file:
        # in file are links of books stored
        for link in file:
            url = link.strip()
            response = requests.get(url)
            if response.ok:
                single_book(url)


# scrape one book:
def single_book(book):
    print("----------start book----------")
    data = [book]
    response = requests.get(book)
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
        # if no description = None
        if description:
            data.append(description)
        else:
            data.append(None)
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

    with open(f"results/{data[1]}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(lines)


get_url()
