



import logging
from urllib.parse import urljoin
import csv
import os
import requests
from bs4 import BeautifulSoup
from lxml import html



logging.basicConfig(level=logging.INFO)

def last_scrap(url_to_scrap, folder):
    response = requests.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "lxml")


    for url in soup.findAll('div', class_='image_container'):
        data = url.findAll('a', href=True)
        for links in data:
            href = links.get("href")
            last_scrap.link = href.replace("../../..", "https://books.toscrape.com/catalogue")
            link = {last_scrap.link}
            for scrap in link:

                response = requests.get(scrap)
                soup = BeautifulSoup(response.content, "lxml")
                data_soup = soup.find_all("td")

                description = soup.find_all("p")[3].text
                upc = data_soup[0].text
                price_exc_tax = data_soup[2].text
                price_inc_tax = data_soup[3].text
                availability = data_soup[5].text
                nb_of_rev = data_soup[6].text
                titres = soup.find("h1").text
                category = soup.find_all("a")[3].text

                for div in soup.find_all('div', class_='item active'):
                    for img in div.findAll('img'):
                        alt = img['alt']
                        source_clean = img['src'].replace("../../", "https://books.toscrape.com/")
                        photo_last_page = open(alt.replace(' ', '-').replace('/', '') + ".jpg", "wb")
                        try:
                            im = requests.get(source_clean)
                            photo_last_page.write(im.content)
                        finally:
                            photo_last_page.close()
                methode_scrap_pagination(url_to_scrap, folder, link, description, upc, price_inc_tax, price_exc_tax,
                                         availability, nb_of_rev, titres, category, source_clean)







def methode_scrap_pagination(url_to_scrap, folder, link, description, upc, price_inc_tax, price_exc_tax, availability, nb_of_rev, titres, category, source_clean):


    response = requests.get(url_to_scrap)

    if response.ok:


        # condition to check if the Next button is available
        logging.info("        Bouton 'Next' detected AND Response: OK       ")
        try:
        # Creat path's folder, the file CSV and Photo are there.
            os.mkdir(os.path.join(os.getcwd(), folder))
        except ValueError:
            logging.debug("Path can't creat")


# Creat file.
        os.chdir(os.path.join(os.getcwd(), folder))
        data_scv = open('dataScrap.csv', 'w', encoding='utf-8', newline='')

# function to creat the file CSV with columns and data.
        try:
            the_writer = csv.writer(data_scv, delimiter=str(';'))
            header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                      'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            the_writer.writerow(header)


# Loop to navigate in pagination
            while True:
                response = requests.get(url_to_scrap)
                soup = BeautifulSoup(response.content, "lxml")
                footer_element = soup.select_one('li.current')
                logging.info(footer_element.text.strip())

# Find next page for pagination
                next_page_element = soup.select_one('li.next > a')
                if next_page_element:
                    next_page_url = next_page_element.get('href')
                    url_to_scrap = urljoin(url_to_scrap, next_page_url)
                    if url_to_scrap:
                        last_scrap(url_to_scrap, folder)
                        data_scrap = [link, upc, titres, price_inc_tax, price_exc_tax, availability,
                                      description, category, nb_of_rev, source_clean]
                        the_writer.writerow(data_scrap)

                # Data scrapped for the last pages
                else:
                    for url in soup.findAll('div', class_='image_container'):

                        for links in url.findAll('a', href=True):
                            href = links.get("href")
                            link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                            for scrap in {link}:
                                soup = BeautifulSoup(requests.get(scrap).content, "lxml")
                                data_soup = soup.find_all("td")


                                description = soup.find_all("p")[3].text
                                upc = data_soup[0].text
                                price_exc_tax = data_soup[2].text
                                price_inc_tax = data_soup[3].text
                                availability = data_soup[5].text
                                nb_of_rev = data_soup[6].text
                                titres = soup.find("h1").text
                                category = soup.find_all("a")[3].text

                                for div in soup.find_all('div', class_='item active'):
                                    for img in div.findAll('img'):
                                        alt = img['alt']
                                        source_clean = img['src'].replace("../../", "https://books.toscrape.com/")
                                        photo_firsts_page = open(alt.replace(' ', '-').replace('/', '') + ".jpg",
                                                                 "wb")
                                        try:
                                            im = requests.get(source_clean)
                                            photo_firsts_page.write(im.content)
                                        finally:
                                            photo_firsts_page.close()

                                    # Data scrapped
                                data_scrap = [link, upc, titres, price_inc_tax, price_exc_tax, availability,
                                              description, category, nb_of_rev, source_clean]
                                the_writer.writerow(data_scrap)


                    break


        finally:
            data_scv.close()
    return logging.info("     Scrapping as been saved     ")

last_scrap("https://books.toscrape.com/catalogue/category/books/childrens_11/index.html", "chffdsfdsffild")



def scrap_for_one_page(url_to_scrap, folder):
    """
    Same code as above for pagination.
    But here we only to check one page without next button.

    """


    response = requests.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "lxml")

    # Test to check is response is ok

    os.mkdir(os.path.join(os.getcwd(), folder))
    if response.ok:

        os.chdir(os.path.join(os.getcwd(), folder))
        file_one_page_scrap = open('Scrap0nePage.csv', 'w', encoding='utf-8', newline='')
        try:

            the_writer = csv.writer(file_one_page_scrap, delimiter=str(';'))
            header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                      'price_excluding_tax',
                      'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            the_writer.writerow(header)

            logging.info("        No bouton 'Next'        ")
            last_scrap(url_to_scrap)
            data_scrap = [last_scrap.link, last_scrap.upc, last_scrap.titres, last_scrap.price_inc_tax,
                          last_scrap.price_exc_tax, last_scrap.availability,
                          last_scrap.description, last_scrap.category, last_scrap.nb_of_rev, last_scrap.source_clean]
            the_writer.writerow(data_scrap)
        finally:
            file_one_page_scrap.close()



        return logging.info("END OF PROGRAM")


#scrap_for_one_page("https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html", "womens")

