"""System module."""
import logging
import csv
import os
import time

from bs4 import BeautifulSoup
import requests


def create_folder(folder: str):
    """
    Create folder containing a csv file with books details and books covers
    :param folder: Name of folder containing data
    :return:
    """
    os.mkdir(os.path.join(os.getcwd(), folder))
    # Setup created folder as active folder
    os.chdir(os.path.join(os.getcwd(), folder))


def get_categories_from_side_bar():
    url = requests.get("https://books.toscrape.com/index.html").text
    soup = BeautifulSoup(url, "html.parser")
    for i in soup.findAll("div", class_="side_categories"):
        for categories_links in i.findAll("div", class_="nav nav-list"):
            links_href = categories_links.get("href")
            formatted_links_categories = f"https://books.toscrape.com/{links_href}"
            text_categories = str(categories_links.get_text())
            block = {text_categories: formatted_links_categories}

            return [block]


def scrape_books(soup):
    """
    This function Scrape all data for each page product,
    also the function downloads all covers of books
    :param soup: BeautifulSoup instance
    """

    book_details_containers = soup.findAll("div", class_="image_container")
    for book_details_url in book_details_containers[0:3]:
        for links in book_details_url.findAll("a", href=True):
            href = links.get("href")
            link = href.replace("../../../", "https://books.toscrape.com/catalogue/")
            logging.info(link)
            soup_scrap = BeautifulSoup(requests.get(link).content, "lxml")
            data_soup = soup_scrap.find_all("td")

            for images in soup_scrap.find_all("img"):
                alt = images.get("alt")
                source_clean = images.get("src").replace(
                    "../../", "https://books.toscrape.com/"
                )

                photo_firsts_page = open(
                    alt.replace(" ", "-").replace("/", "") + ".jpg", "wb"
                )  # pylint: disable=bad-option-value
                image_response = requests.get(source_clean)
                photo_firsts_page.write(image_response.content)
                photo_firsts_page.close()

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


def write_to_csv(extracted_books: list):
    """
    Write books into csv,
    :param extracted_books: Books details scraped previously
    :return:
    """
    csv_file = open("dataScrap.csv", "w", encoding="utf-8", newline="")
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
    writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=str(";"))
    writer.writeheader()
    writer.writerows(extracted_books)
    csv_file.close()


def browse_and_scrape(url: str, folder: str, page_number: int = 1) -> bool:
    """
    Scrape all books from website 'books to scrape'
    :param url: Url of the first page to scrape
    :param folder: Folder name containing scraped data and photos
    :param page_number: Number page origin
    :return:
    """
    try:
        formatted_url = url.replace(
            "books.toscrape.com/index.html",
            f"books.toscrape.com/catalogue/page-{page_number}.html",
        )
        html_text = requests.get(formatted_url).text
        soup = BeautifulSoup(html_text, "html.parser")
        logging.info("Now Scraping %s", formatted_url)
        if soup.find("li", class_="next") is not None:
            scrape_books(soup)
            time.sleep(3)
            page_number += 1
            browse_and_scrape(url, folder, page_number)
        elif soup.find("li", class_="next") is None:
            scrape_books(soup)
            return True
        return True
    except Exception as ex:
        logging.error(ex)
        raise ex


def scrape_book_for_category(category):
    """
    Scrape book for category
    :param : category name
    :return:
    """
    name = category["name"]
    create_folder(name)
    # result = browse_and_scrape(category["url"], name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # category_url = input("url to scrape : ")
    books = []

    # target_folder = input("folder name to store books info :")
    logging.info("Web scraping starting")
    categories = [
        {
            "name": "Category",
            "url": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        },
        {
            "name": "Category2",
            "url": "https://books.toscrape.com/catalogue/category/books/crime_51/index.html",
        },
    ]
    for cate in categories:
        scrape_book_for_category(cate)
