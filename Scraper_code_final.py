# TODO: Rename file to scraper

# TODO: Delete comments 'Import Moduls' not needed
# TODO: Install pre-commit which will help you to check for unused imports

# TODO: Make sure this is working to scrape all the books for all categories

##############################
#        Import Moduls       #
import logging
import csv
import requests
from bs4 import BeautifulSoup
# TODO: os, time imports should be before bs4. Please install pylint
import os
import time
<<<<<<< Updated upstream
# TODO: Delete unused import
import re
=======
>>>>>>> Stashed changes


logging.basicConfig(level=logging.INFO)

<<<<<<< Updated upstream
# TODO: Rename to create_folder
# TODO: folder is a string in the signature
# TODO: Add a docstring
# TODO: I don't think the try except is needed here since your are creating your folder at the beginning
# TODO: What is doing os.chdir
def creat_folder(folder):
=======
def creat_folder(folder: str):
    """
    this function creat folder where we will have a file csv and photos
    :param folder: name of folder's data, entered by the user
    :return:
    """
>>>>>>> Stashed changes
    try:
        # Creat path's folder, the file CSV and Photo are there.

        os.mkdir(os.path.join(os.getcwd(), folder))
    except ValueError:
        logging.debug("Path can't creat")
        # Creat file.
    os.chdir(os.path.join(os.getcwd(), folder))


<<<<<<< Updated upstream
# TODO: Rename to scrape_books
# TODO: Add types in signature for formatted_url and soup
def scrap(formatted_url, soup):

=======
def scrap(formatted_url: str, soup):
    """
    This function Scrape all data for each page product,
    also th function download all picture of books
    :param formatted_url: url formatted_url for pagination
    :param soup: variable to invoke BeautifulSoup module
    :return:
    """
>>>>>>> Stashed changes
    container = soup.findAll('div', class_='image_container')
    for i in container:
        for links in i.findAll('a', href=True):
            href = links.get("href")
            link = 'https://books.toscrape.com/catalogue/' + href
            for scraps in {link}:
                soup_scrap = BeautifulSoup(requests.get(scraps).content, "lxml")
                data_soup = soup_scrap.find_all("td")
                for images in soup_scrap.find_all("img"):
                    alt = images.get('alt')
                    source_clean = images.get('src').replace("../../", "https://books.toscrape.com/")
                    print(source_clean)
                    photo_firsts_page = open(alt.replace(' ', '-').replace('/', '') + ".jpg", "wb")
                    try:
                        im = requests.get(source_clean)
                        photo_firsts_page.write(im.content)
                    finally:
                        photo_firsts_page.close()

                book = {'product_page_url': link,
                        'universal_product_code': data_soup[0].text,
                        'title': soup_scrap.find("h1").text,
                        'price_including_tax': data_soup[3].text,
                        'price_excluding_tax': data_soup[2].text,
                        'number_available': data_soup[6].text,
                        'product_description': soup_scrap.find_all("p")[3].text,
                        'category': soup_scrap.find_all("a")[3].text,
                        'review_rating': data_soup[5].text,
                        'image_source_url': source_clean,
                        }
                books.append(book)
        write_to_csv(books)
# TODO: Delete uneccessary spaces



# TODO: Add type for books in signature
# TODO: I don't think the try except is necessary here because you control well what your code is doing
def write_to_csv(books):
    """
    Write books into csv
    :param books:
    :return:
    """
    data_scv = open('dataScrap.csv', 'w', encoding='utf-8', newline='')
    try:
        header = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                  'price_excluding_tax',
                  'number_available', 'product_description', 'category', 'review_rating', 'image_source_url']
        writer = csv.DictWriter(data_scv, fieldnames=header, delimiter=str(';'))
        writer.writeheader()
        writer.writerows(books)
    except:
        return False

<<<<<<< Updated upstream
# TODO: Add docstring
# TODO: Add type for page_number
# TODO: Doesnt return str return a boolean True if good
# TODO: Raise exception if not good
# TODO: Use logging not print
# TODO: Delete commented code which is not used
def browse_and_scrape(url: str, page_number=1) -> str:


    #url_one_scrap = url.replace('index.html', ' ')
    try:
        #creat_folder(folder)
        # TODO: You need to find a way working to scrape all the books from
        formatted_url = url.replace('index', f'page-{page_number}')
=======



def browse_and_scrape(url: str, folder: str, page_number: int = 1) -> str:
    """
    Scrape all books from website 'books to scrape'
    :param url of first category page
    :param page_number: number page origin
    :return:
    """
    try:
        formatted_url = url.replace('books.toscrape.com/index.html', f'books.toscrape.com/catalogue/page-{page_number}.html')
>>>>>>> Stashed changes
        html_text = requests.get(formatted_url).text
        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Now Scraping - {formatted_url}")
        if soup.find("li", class_='next') is not None:
            scrap(formatted_url, soup)
            time.sleep(3)
            page_number += 1
            browse_and_scrape(url, folder, page_number)
        elif soup.find("li", class_='next') is None:
            scrap(formatted_url, soup)
            return True
        return True
    except Exception as e:
        raise e


if __name__ == "__main__":
    url = input('url to scrap : ')
    books = []
    print("Web scraping has begun")
    folder = input('le nom du dossier :')
    creat_folder(folder)
    result = browse_and_scrape(url, folder)
    if result == True:
        logging.info("Web scraping is now complete!")
    else:
        logging.info(f"Oops, That doesn't seem right!!! - {result}")