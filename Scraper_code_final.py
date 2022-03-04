##############################
#        Import Moduls       #
import logging
import csv
import requests
from bs4 import BeautifulSoup
import os
import time
import re



books = []
logging.basicConfig(level=logging.INFO)

def creat_folder(folder):
    try:
        # Creat path's folder, the file CSV and Photo are there.
        os.mkdir(os.path.join(os.getcwd(), folder))
    except ValueError:
        logging.debug("Path can't creat")

        # Creat file.
    os.chdir(os.path.join(os.getcwd(), folder))


def scrap(formatted_url, soup):

    container = soup.findAll('div', class_='image_container')
    for i in container:

        for links in i.findAll('a', href=True):
            href = links.get("href")
            link = href.replace("../../..", "https://books.toscrape.com/catalogue")
            for scraps in {link}:
                soup_scrap = BeautifulSoup(requests.get(scraps).content, "lxml")
                data_soup = soup_scrap.find_all("td")


                book = {'product_page_url': link,
                        'universal_product_code': data_soup[0].text,
                        'title': soup_scrap.find("h1").text,
                        'price_including_tax': data_soup[3].text,
                        'price_excluding_tax': data_soup[2].text,
                        'number_available': data_soup[6].text,
                        'product_description': soup_scrap.find_all("p")[3].text,
                        'category': soup_scrap.find_all("a")[3].text,
                        'review_rating': data_soup[5].text
                        }

                books.append(book)
        write_to_csv(books)





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
                  'number_available', 'product_description', 'category', 'review_rating']
        writer = csv.DictWriter(data_scv, fieldnames=header, delimiter=str(';'))
        writer.writeheader()
        writer.writerows(books)
    except:
        return False




def browse_and_scrape(url: str, page_number=1) -> str:


    #url_one_scrap = url.replace('index.html', ' ')
    try:
        #creat_folder(folder)
        formatted_url = url.replace('index', f'page-{page_number}')
        html_text = requests.get(formatted_url).text
        soup = BeautifulSoup(html_text, "html.parser")

        print(f"Now Scraping - {formatted_url}")

        if soup.find("li", class_='next') is not None:
            scrap(formatted_url, soup)
            time.sleep(3)
            page_number += 1
            browse_and_scrape(url, page_number)
        elif soup.find("li", class_='next') is None:
            scrap(formatted_url, soup)
            return True
        return True
    except Exception as e:
        return e




if __name__ == "__main__":
    url = input('url to scrap : ')
    print("Web scraping has begun")
    result = browse_and_scrape(url)
    if result == True:
        print("Web scraping is now complete!")
    else:
        print(f"Oops, That doesn't seem right!!! - {result}")