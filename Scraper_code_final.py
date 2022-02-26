##############################
# Program Python Type        #
# author : Mekki GreyHat     #
# Licence : OC               #
##############################


##############################
#        Import Moduls       #

import logging
from urllib.parse import urljoin
import csv
import os
import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import time


url = 'https://books.toscrape.com/catalogue/category/books/romance_8/index.html'



logging.basicConfig(level=logging.INFO)
# Delete spaces
"""
def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup



def creat_folder(folder):
    try:
        # Creat path's folder, the file CSV and Photo are there.
        os.mkdir(os.path.join(os.getcwd(), folder))
    except ValueError:
        logging.debug("Path can't creat")

        # Creat file.
    os.chdir(os.path.join(os.getcwd(), folder))
"""


def scrap(url, soup):
    books = []
    container = soup.findAll('div', class_='image_container')
    for i in container:
        for links in i.findAll('a', href=True):
            href = links.get("href")
            link = href.replace("../../..", "https://books.toscrape.com/catalogue")
            for scrap in {link}:
                soup_scrap = BeautifulSoup(requests.get(scrap).content, "lxml")
                data_soup = soup_scrap.find_all("td")

                book = {'description': soup_scrap.find_all("p")[3].text,
                        'upc': data_soup[0].text,
                        'price_exc_tax': data_soup[2].text,
                        'price_inc_tax': data_soup[3].text,
                        'availability': data_soup[5].text,
                        'nb_of_rev': data_soup[6].text,
                        'titres': soup_scrap.find("h1").text,
                        'category': soup_scrap.find_all("a")[3].text}
                books.append(book)
    write_to_csv(books)




def write_to_csv(books: list):
    """
    Write books into csv
    :param books:
    :return:
    """
    data_scv = open('dataScrap.csv', 'w', encoding='utf-8', newline='')
    try:

        header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                  'price_excluding_tax',
                  'number_available', 'product_description', 'category', 'review_rating']
        writer = csv.DictWriter(data_scv, header)
        writer.writeheader()
        writer.writerows(books)
    except ValueError:
        return




def browse_and_scrape(url, page_number=1):

    formatted_url = url.replace('index', f'page-{page_number}')
    try:
        html_text = requests.get(formatted_url).text

        soup = BeautifulSoup(html_text, "html.parser")
        print(f"Now Scraping - {formatted_url}")

        if soup.find("li", class_='next') != None:

            scrap(url, soup)
            time.sleep(3)
            page_number += 1

            browse_and_scrape(url, page_number)
        else:
            scrap(url, soup)
            return True
        return True
    except Exception as e:
        return e




if __name__ == "__main__":
    url = 'https://books.toscrape.com/catalogue/category/books/romance_8/index.html'
    print("Web scraping has begun")
    result = browse_and_scrape(url)
    if result == True:
        print("Web scraping is now complete!")
    else:
        print(f"Oops, That doesn't seem right!!! - {result}")



















"""

def scrap_in_page(soup):

    container = soup.findAll('div', class_='image_container')
    for i in container:
        for links in i.findAll('a', href=True):
            href = links.get("href")
            link = href.replace("../../..", "https://books.toscrape.com/catalogue")
            for scrap in {link}:
                soup_scrap = BeautifulSoup(requests.get(scrap).content, "lxml")
                data_soup = soup_scrap.find_all("td")

                description = soup_scrap.find_all("p")[3].text
                upc = data_soup[0].text
                price_exc_tax = data_soup[2].text
                price_inc_tax = data_soup[3].text
                availability = data_soup[5].text
                nb_of_rev = data_soup[6].text
                titres = soup_scrap.find("h1").text
                category = soup_scrap.find_all("a")[3].text

                data_scrap = link, upc, titres, price_inc_tax, price_exc_tax, availability, description, category, nb_of_rev


            yield data_scrap

soup = get_data(url)




def main(url):
    data_scv = open('dataScrap.csv', 'w', encoding='utf-8', newline='')
    try:
        the_writer = csv.writer(data_scv, delimiter=str(';'))
        header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
              'price_excluding_tax',
              'number_available', 'product_description', 'category', 'review_rating']
        the_writer.writerow(header)
        while True:

            next_page_element = soup.select_one('li.next > a')
            if next_page_element is not None:
                next_page_url = next_page_element.get('href')
                url = urljoin(url, next_page_url)
                print(url)
                tableau = []
                for item in scrap_in_page(soup):
                    tableau.append(item)
                    the_writer.writerow(item)
            else:
                tableau = []
                for item in scrap_in_page(soup):
                    tableau.append(item)
                    the_writer.writerow(item)
                break

    finally:
        data_scv.close()
        return


main(url)



#print(scrap_in_page(soup))



récupérer toutes les valeurs du tableau pour afficher ceci dans le reste du code
for item in scrap_in_page(soup):
print(item)
"""
