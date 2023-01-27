from book_scrape import category_scrape, scrape_links_of_books_in_category, info_from_category


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # start the program:
    # get first all categories with category_scrape:
    all_categories = category_scrape()
    links = scrape_links_of_books_in_category(all_categories)
    info_from_category(links)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
