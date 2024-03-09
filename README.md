# Book to Scrape

## Description:
Project 2 of OpenClassrooms Path: Developer Python - Book to Scrape 
-- extract certain information of http://books.toscrape.com into a csv file:

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

These information should be extracted for each single book. Organised in the category on the website.

**An improved version (2.0) is available in branch `dev/version-2.0`**

## Installation:
open terminal
1. `git clone https://github.com/DoriDoro/Book_to_Scrape.git`
2. `cd Book_to_Scrape`
3. `python -m venv venv`
4. `. venv/bin/activate` (on MacOS/Linux)  `venv\Scripts\activate` (on Windows)
5. `pip install -r requirements.txt`


## Skills:
- Configuring a Python environment
- Managing data using the ETL process
- Using version control with Git and GitHub
- Applying the basics of Python programming


## Visualisation of the project:
start the program with `python3 main.py`

in terminal you will see: <br>
![terminal](/images_Readme/Terminal.png)

the results are visible in following folders:
1. the results of the images: <br>
![images](/images_Readme/ResultsImages.png)
2. the csv files: <br>
![csv](/images_Readme/ResultsResults.png)