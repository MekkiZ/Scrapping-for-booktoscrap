"""System module."""
import logging
import csv
import os
import time
from bs4 import BeautifulSoup
import requests


def creat_folder(folder: str):
    """
    this function creat folder where we will have a file csv and photos
    :param folder: name of folder's data, entered by the user
    :return:
    """
    try:
        # Creat path's folder, the file CSV and Photo are there.
        os.mkdir(os.path.join(os.getcwd(), folder))
    except ValueError:
        logging.debug("Path can't creat")
        # Creat file in the root's project.
    os.chdir(os.path.join(os.getcwd(), folder))


def scrape_books(soup):
    """
    This function Scrape all data for each page product,
    also th function download all picture of books
    :param soup: variable to invoke BeautifulSoup module
    """
    container = soup.findAll("div", class_="image_container")
    for i in container:
        for links in i.findAll("a", href=True):
            href = links.get("href")
            link = "https://books.toscrape.com/catalogue/" + href
            for scraps in {link}:
                soup_scrap = BeautifulSoup(requests.get(scraps).content, "lxml")
                data_soup = soup_scrap.find_all("td")

                for images in soup_scrap.find_all("img"):
                    alt = images.get("alt")
                    source_clean = images.get("src").replace(
                        "../../", "https://books.toscrape.com/"
                    )
                    photo_firsts_page = open(
                        alt.replace(" ", "-").replace("/", "") + ".jpg", "wb"
                    )
                    try:
                        image_response = requests.get(source_clean)
                        photo_firsts_page.write(image_response.content)
                    finally:
                        photo_firsts_page.close()
                        source_clean = images.get("src").replace(
                            "../../", "https://books.toscrape.com/"
                        )

                book = {
                    "product_page_url": link,
                    "universal_product_code": data_soup[0].text,
                    "title": soup_scrap.find("h1").text,
                    "price_including_tax": data_soup[3].text,
                    "price_excluding_tax": data_soup[2].text,
                    "number_available": data_soup[6].text,
                    "product_description": soup_scrap.find_all("p")[3].text,
                    "category": soup_scrap.find_all("a")[3].text,
                    "review_rating": data_soup[5].text,
                    "image_source_url": source_clean,
                }
                books.append(book)
        write_to_csv(books)


def write_to_csv(book_from_scrap: list):
    """
    Write books into csv
    :param book_from_scrap: data from dict scraped previously
    :return:
    """
    data_scv = open("dataScrap.csv", "w", encoding="utf-8", newline="")
    header = [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_source_url",
    ]
    writer = csv.DictWriter(data_scv, fieldnames=header, delimiter=str(";"))
    writer.writeheader()
    writer.writerows(book_from_scrap)


def browse_and_scrape(url: str, folder: str, page_number: int = 1) -> str:
    """
    Scrape all books from website 'books to scrape'
    :param url of first category page
    :param folder is the localisation for data scraped and photos
    :param page_number: number page origin
    :return:
    """
    try:
        formatted_url = url.replace(
            "books.toscrape.com/index.html",
            f"books.toscrape.com/catalogue/page-{page_number}.html",
        )
        html_text = requests.get(formatted_url).text
        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Now Scraping - {formatted_url}")
        if soup.find("li", class_="next") is not None:
            scrape_books(soup)
            time.sleep(3)
            page_number += 1
            browse_and_scrape(url, folder, page_number)
        elif soup.find("li", class_="next") is None:
            scrape_books(soup)
            return str(True)
        return str(True)
    except Exception as ex:
        raise ValueError from ex


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    url_to_scrap = input("url to scrap : ")
    books = []
    folders = input("le nom du dossier :")
    print("Web scraping has begun")
    creat_folder(folders)
    RESULT = browse_and_scrape(url_to_scrap, folders)
    if RESULT is True:
        logging.info("Web scraping is now complete!")
    else:
        print(f"Oops, That doesn't seem right!!! - {RESULT}")
