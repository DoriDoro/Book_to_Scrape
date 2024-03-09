# coding=utf-8
# -*- coding: utf-8 -*-

import csv
import os

import wget
import re
import requests

from bs4 import BeautifulSoup as BfS


def get_category_links(url):
    """
    Fetches and returns links to all book categories from the given URL.

    Args:
        url (str): The base URL to scrape book categories from.

    Returns:
        list: A list of URLs representing the book categories.
    """

    category_links = []

    try:
        response = requests.get(url)
        if not response.ok:
            print("Failed to retrieve categories:", response.status_code)
            return category_links

        soup = BfS(response.content, "html.parser")
        categories = soup.select(".side_categories a")

        for category in categories:
            href = category.get("href")
            if href and "catalogue/category/books_1" not in href:
                category_links.append(url + href)
    except Exception as e:
        print("An error occurred while fetching category links:", str(e))

    return category_links


def scrape_category_pages(category_url):
    """
    Scrapes and returns links to all pages of a given category.

    Args:
        category_url (str): The URL of the category to scrape.

    Returns:
        list: A list of URLs representing the pages of the category.
    """

    page_links = []

    try:
        response = requests.get(category_url)
        if not response.ok:
            print("Failed to retrieve category page:", response.status_code)
            return page_links

        soup = BfS(response.content, "html.parser")
        next_page = soup.find("ul", class_="pager")

        if next_page:
            current_page = int(next_page.find("li", class_="current").text.strip()[10:])
            page_links.append(category_url)

            for page_num in range(2, current_page + 1):
                page_links.append(category_url.replace('index.html', f'page-{page_num}.html'))
    except Exception as e:
        print("An error occurred while scraping category pages:", str(e))

    return page_links


def category_scrape():
    """
    Scrape and return links to all book categories and their pages.

    Returns:
        list: A list of URLs representing book categories and their pages.
    """
    print("---------- starting program ----------")
    print(" Please wait ... ")
    base_url = "http://books.toscrape.com/"
    all_category_links = []

    try:
        category_links = get_category_links(base_url)

        for category_link in category_links:
            all_category_links.extend(scrape_category_pages(category_link))

    except Exception as e:
        print("An error occurred during category scraping:", str(e))

    return all_category_links


def get_book_links_from_page(page_url):
    """
    Fetches and returns links to books from a given page URL.

    Args:
        page_url (str): The URL of the page containing book links.

    Returns:
        list: A list of URLs representing the books on the page.
    """
    book_links = []
    try:
        response = requests.get(page_url)
        if not response.ok:
            print(f"Failed to retrieve books from {page_url}: {response.status_code}")
            return book_links

        soup = BfS(response.content, "html.parser")
        articles = soup.find_all("article", class_="product_pod")
        book_links = [
            f'http://books.toscrape.com/catalogue/{article.find("a")["href"].replace("../../../", "")}'
            for article in articles]
    except Exception as e:
        print(f"An error occurred while fetching book links from {page_url}: {str(e)}")

    return book_links


def scrape_links_of_books_in_category(category_links, show_progress=True):
    """
    Scrape and return links to books in the specified categories.

    Args:
        category_links (list): A list of URLs representing book categories.
        show_progress (bool): Whether to display a progress indicator.

    Returns:
        list: A list of URLs representing books in the specified categories.
    """

    books_in_category = []
    total_categories = len(category_links)

    for index, category_link in enumerate(category_links, start=1):
        if show_progress:
            print(f"Scraping category {index}/{total_categories}")

        book_links = get_book_links_from_page(category_link)
        books_in_category.extend(book_links)

    return books_in_category


def single_book_scrape(book_url):
    """
    Scrapes information about a single book from its URL.

    Args:
        book_url (str): The URL of the book to scrape.

    Returns:
        dict: A dictionary containing information about the book.
    """

    try:
        response = requests.get(book_url)
        if not response.ok:
            print(f"Failed to fetch book data from {book_url}: {response.status_code}")
            return None

        soup = BfS(response.content, "html.parser")

        image = soup.find("img")
        image_url = image.get("src").replace("../../", "http://books.toscrape.com/")
        title = image.get("alt")
        upc = get_book_info(soup, "UPC")
        pit = get_book_info(soup, "Price (incl. tax)")
        pet = get_book_info(soup, "Price (excl. tax)")
        available = get_book_info(soup, "Availability", strip_text="In stock ()")
        description = get_book_description(soup)
        category = get_book_category(soup)
        rating = get_book_rating(soup)

        data = {
            "link": book_url,
            "universal_product_code": upc,
            "title": title,
            "price_including_tax": pit,
            "price_excluding_tax": pet,
            "number_available": available,
            "product_description": description,
            "category": category,
            "review_rating": rating,
            "image_url": image_url
        }

        return data
    except Exception as e:
        print(f"An error occurred while scraping book data: {str(e)}")
        return None


def get_book_info(soup, label, strip_text=""):
    """
    Extracts information about a book based on the given label from the book's HTML soup.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the book's HTML.
        label (str): The label identifying the desired information.
        strip_text (str): Optional text to strip from the extracted information.

    Returns:
        str: The extracted information, or None if not found.
    """
    try:
        info = soup.find("th", text=label).find_next_sibling("td").get_text(strip=True)
        if strip_text:
            info = info.replace(strip_text, "")
        return info
    except AttributeError:
        print(f"No information found for '{label}'")
        return None


def get_book_description(soup):
    """
    Extracts the description of a book from its HTML soup.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the book's HTML.

    Returns:
        str: The description of the book, or None if not found.
    """
    try:
        description = soup.find("div", id="product_description").find_next("p").get_text(
            strip=True)
        return description
    except AttributeError:
        print("No description found for this book.")
        return None


def get_book_category(soup):
    """
    Extracts the category of a book from its HTML soup.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the book's HTML.

    Returns:
        str: The category of the book, or None if not found.
    """
    try:
        category = soup.find("a", href=re.compile("/category/books/")).get_text(strip=True)
        return category
    except AttributeError:
        print("No category found for this book.")
        return None


def get_book_rating(soup):
    """
    Extracts the rating of a book from its HTML soup.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the book's HTML.

    Returns:
        str: The rating of the book, or None if not found.
    """
    try:
        rating_class = soup.find("p", class_="star-rating")["class"][1]
        rating = rating_class.replace("star-rating", "").strip()
        return rating
    except AttributeError:
        print("No rating found for this book.")
        return None


def get_image(image_url, category_name):
    """
    Downloads the image from the given URL and saves it in the appropriate category folder.

    Args:
        image_url (str): The URL of the image to download.
        category_name (str): The name of the category folder to save the image in.
    """
    try:
        image_path = f"images/{category_name}"
        os.makedirs(image_path, exist_ok=True)

        image_filename = os.path.basename(image_url)
        image_filepath = os.path.join(image_path, image_filename)

        if not os.path.exists(image_filepath):
            wget.download(image_url, out=image_filepath)
            print(f" Downloaded image: {image_url}")
        else:
            print(f" Image already exists: {image_url}")
    except Exception as e:
        print(f" Error downloading image from {image_url}: {e}")


def info_from_category(links):
    """
    Scrapes information for each book in the specified category.

    Args:
        links (list): A list of book URLs.

    Returns:
        list: A list of dictionaries containing book information.
    """
    information = []
    for link in links:
        book_info = single_book_scrape(link)
        information.append(book_info)

        try:
            get_image(book_info['image_url'], book_info['category'])
        except KeyError:
            print(f"No image URL found for book: {book_info}")

        write_csv(information, book_info['category'])
    return information


def write_csv(data, category_name):
    """
    Writes book information to a CSV file for the specified category.

    Args:
        data (list): A list of dictionaries containing book information.
        category_name (str): The name of the category.
        header (list, optional): The header row for the CSV file. Defaults to None.
    """
    if not isinstance(data, list):
        raise ValueError("Data must be a list of dictionaries")

    if not all(isinstance(entry, dict) for entry in data):
        raise ValueError("Each entry in data must be a dictionary")

    header = [
        "Product Page URL",
        "Image URL",
        "Title",
        "Universal Product Code",
        "Price including tax",
        "Price excluding tax",
        "Number available",
        "Category",
        "Review Rating",
        "Product Description"
    ]

    try:
        folder_path = f"results/{category_name}"
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{category_name}.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            write = csv.DictWriter(file, fieldnames=header)
            write.writeheader()
            for one_book in data:
                write.writerow({'Product Page URL': one_book['link'],
                                'Universal Product Code': one_book['universal_product_code'],
                                'Title': one_book['title'],
                                'Price including tax': one_book['price_including_tax'],
                                'Price excluding tax': one_book['price_excluding_tax'],
                                'Number available': one_book['number_available'],
                                'Product Description': one_book['product_description'],
                                'Category': one_book['category'],
                                'Review Rating': one_book['review_rating'],
                                'Image URL': one_book['image_url']})

        print(f"CSV file successfully created: {file_path}")
    except Exception as e:
        print(f"Error writing CSV file: {str(e)}")
