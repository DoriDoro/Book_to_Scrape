# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import re
import requests

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

            if not href == "catalogue/category/books_1/index.html":
                response = requests.get(link)
                if response.ok:
                    soup = BfS(response.content, "html.parser")
                    next_page = soup.findAll('ul', class_='pager')
                    if next_page:
                        for page in next_page:
                            all_num_page = page.find("li", class_="current").text
                            num_page = int(all_num_page.strip()[10:])

                            counter = 2
                            while num_page > 1:
                                link_next_page = f"{link.replace('index.html', '')}page-{counter}.html"
                                links_of_categories_all.append(link_next_page)
                                num_page -= 1
                                counter += 1
        # start from the second:
        links_of_categories = links_of_categories_all[1:]

        # scrape all links of the books
        scrape_links_of_books_in_category(links_of_categories)


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
            # find the category name:
            div_title = soup.find("div", class_="page-header")
            get_name_of_category = div_title.find("h1").text
            name_of_category = get_name_of_category.lower()

            # find all <article class="product_pod">:
            articles = soup.find_all("article", class_="product_pod")
            for article in articles:
                a = article.find("a")
                a_link = a["href"]
                # create link of each book:
                books_in_category.append(f'http://books.toscrape.com/catalogue/{a_link.replace("../../../", "")}')

                for book in books_in_category:
                    # scrape the single book:
                    single_book(book)

            # write all books from each category in csv file:
            append_csv_link(books_in_category, name=f"books_in_cat_{name_of_category}")


# append links as row data in csv file:
def append_csv_link(links, name):
    with open(f"results/{name}.csv", "a", newline="", encoding="utf-8") as file:
        for link in links:
            writer = csv.writer(file)
            writer.writerow([link])


# scrape one book:
def single_book(book):
    print("----------start book----------")
    data = [book]
    response = requests.get(book)
    if response.ok:
        soup = BfS(response.content, "html.parser")
        # search for information on website:
        # image
        image = soup.find("img")
        image_url = image["src"]
        data.append(image_url.replace("../..", "http://books.toscrape.com"))
        # title: at image tag use alt attribute
        title_side = image["alt"]
        title = title_side.replace(":", "")
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
        description = soup.find("p").string
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

        write_csv(data)


def write_csv(data):
    # write information in csv-file:
    header = ["Product Page URL", "Universal Product Code", "Title", "Price including tax", "Price excluding tax",
              "Number available", "Product Description", "Category", "Review Rating", "Image URL"]
    lines = [data]

    with open(f"results/{data[2]}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(lines)


category_scrape()
