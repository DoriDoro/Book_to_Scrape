# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import wget
import re
import requests

from pathlib import Path
from bs4 import BeautifulSoup as BfS


# scrape all links of the categories even for multiple pages:
def category_scrape():
    print("----------start category----------")
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    if response.ok:
        # create a list for all links of the categories:
        links_of_categories_all = []

        soup = BfS(response.content, "html.parser")
        # take information for the sidebar: categories
        categories = soup.select(".side_categories a")
        for category in categories:
            href = category["href"]
            link = f"http://books.toscrape.com/{href}"
            # create one link of each book:
            links_of_categories_all.append(link)

            # start from the second link, start with Travel:
            if not href == "catalogue/category/books_1/index.html":
                response = requests.get(link)
                if response.ok:
                    soup = BfS(response.content, "html.parser")
                    # check if for a next page, take the info: page 1 of 2:
                    next_page = soup.findAll('ul', class_='pager')
                    if next_page:
                        for page in next_page:
                            all_num_page = page.find("li", class_="current").text
                            # get the last number of info, to know how many pages will be there:
                            num_page = int(all_num_page.strip()[10:])

                            counter = 2
                            while num_page > 1:
                                link_next_page = f"{link.replace('index.html', '')}page-{counter}.html"
                                links_of_categories_all.append(link_next_page)
                                num_page -= 1
                                counter += 1

        # start from the second link in the list:
        links_of_categories = links_of_categories_all[1:]

        return links_of_categories


# get all links of the books in one category:
def scrape_links_of_books_in_category(category_links):
    print("----------start books in category----------")
    # read information to get the book links of each book in one category:
    for link in category_links:
        book_url = link.strip()
        response = requests.get(book_url)
        if response.ok:
            # create a list for all links of books inside a category:
            books_in_category = []
            soup = BfS(response.content, "html.parser")
            # find all <article class="product_pod">:
            articles = soup.find_all("article", class_="product_pod")
            for article in articles:  # for books in category:
                a = article.find("a")
                a_link = a["href"]
                # create link of each book:
                books_in_category.append(f'http://books.toscrape.com/catalogue/{a_link.replace("../../../", "")}')

            return books_in_category


# scrape one book:
def single_book_scrape(book):
    print("----------start book----------")
    response = requests.get(book)
    if response.ok:
        soup = BfS(response.content, "html.parser")
        # search for information on website:
        # image
        image = soup.find("img")
        image_url = image["src"]
        image_url = image_url.replace("../../", "http://books.toscrape.com/")
        # title: at image tag use alt attribute
        title = image["alt"]
        # universal product code (upc)
        upc = soup.find("th", text="UPC").find_next_sibling("td").string
        # price including tax (pit)
        pit = soup.find("th", text="Price (incl. tax)").find_next_sibling("td").string
        # price_excluding_tax (pet)
        pet = soup.find("th", text="Price (excl. tax)").find_next_sibling("td").string
        # available number
        get_available = soup.find("th", text="Availability").find_next_sibling("td").string
        available = get_available.replace("In stock (", "").replace(")", "")
        # product description
        description = soup.find("div", id="product_description").find_next("p").string
        # if no description = None
        if description:
            description = description
        else:
            description = None
        # category
        get_category = soup.find("a", attrs={"href": re.compile("/category/books/")}).string
        # category = get_category.lower().replace(" ", "-")
        # review rating
        rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]

        # save data of one single book in dictionary data:
        data = {"link": book, "universal_product_code": upc, "Title": title, "price_including_tax": pit,
                "price_excluding_tax": pet, "number_available": available, "product_description": description,
                "category": get_category, "review_rating": rating, "image_url": image_url}

        return data


def get_image(image_url, name_category):
    path = f"images/{name_category}"
    Path(path).mkdir(parents=True, exist_ok=True)
    # download the image:
    wget.download(image_url, path, bar=None)


def info_from_category(liens):
    infos = []
    for link in liens:
        livre_info = single_book_scrape(link)
        infos.append(livre_info)
        get_image(livre_info['image_url'], livre_info['category'])
    return infos


# write information in csv-file:
def write_csv(datas, category_name):  # data is a list
    header = ["Product Page URL", "Image URL", "Title", "Universal Product Code", "Price including tax",
              "Price excluding tax", "Number available", "Category", "Review Rating", "Product Description"]

    with open(f"results/{category_name}.csv", "w", newline="", encoding="utf-8") as file:
        write = csv.DictWriter(file, fieldnames=header)
        write.writeheader()
        for one_book in datas:
            write.writerow({'Product Page URL': one_book['link'],
                            'Universal Product Code': one_book['universal_product_code'],
                            'Title': one_book['Title'],
                            'Price including tax': one_book['price_including_tax'],
                            'Price excluding tax': one_book['price_excluding_tax'],
                            'Number available': one_book['number_available'],
                            'Product Description': one_book['product_description'],
                            'Category': one_book['category'],
                            'Review Rating': one_book['review_rating'],
                            'Image URL': one_book['image_url']})


liens = scrape_links_of_books_in_category(category_scrape())
info = info_from_category(liens)
write_csv(info, "travel")
