##############################
# Program Python Type        #
# author : Mekki GreyHat     #
# Licence : OC               #
##############################


##############################
#        Import Moduls       #

import logging
import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urljoin
import csv
import os


logging.basicConfig(level=logging.INFO)





def methode_scrap_pagination(url_to_scrap, folder):

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
                        for url in soup.findAll('div', class_='image_container'):
                            for links in url.findAll('a', href=True):
                                href = links.get("href")
                                link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                                tableau = {link}
                                for scrap in tableau:
                                    soup = BeautifulSoup(requests.get(scrap).content, "lxml")

                                    description = soup.find_all("p")[3].text
                                    upc = soup.find_all("td")[0].text
                                    price_exc_tax = soup.find_all("td")[2].text
                                    price_inc_tax = soup.find_all("td")[3].text
                                    availability = soup.find_all("td")[5].text
                                    nb_of_rev = soup.find_all("td")[6].text
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
                else:
                    for url in soup.findAll('div', class_='image_container'):
                        data = url.findAll('a', href=True)
                        for links in data:
                            href = links.get("href")
                            link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                            tableau = {link}
                            for scrap in tableau:
                                response = requests.get(scrap)
                                soup = BeautifulSoup(response.content, "lxml")

                                description = soup.find_all("p")[3].text
                                upc = soup.find_all("td")[0].text
                                price_exc_tax = soup.find_all("td")[2].text
                                price_inc_tax = soup.find_all("td")[3].text
                                availability = soup.find_all("td")[5].text
                                nb_of_rev = soup.find_all("td")[6].text
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

                                # Data scrapped
                                data_scrap = [link, upc, titres, price_inc_tax, price_exc_tax, availability,
                                            description, category, nb_of_rev, source_clean]
                                the_writer.writerow(data_scrap)



                    break


        finally:
            data_scv.close()
    return logging.info("     Scrapping as been saved     ")





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
            for art in soup.findAll('div', class_='image_container'):
                lien = art.findAll('a', href=True)
                for liens in lien:
                    href = liens.get("href")
                    link_one_page = href.replace("../../..", "https://books.toscrape.com/catalogue")
                    table = {link_one_page}
                    for scrap in table:
                        res = requests.get(scrap)
                        soup = BeautifulSoup(res.content, "lxml")

                        description = soup.find_all("p")[3].text
                        upc = soup.find_all("td")[0].text
                        price_exc_tax = soup.find_all("td")[2].text
                        price_inc_tax = soup.find_all("td")[3].text
                        availability = soup.find_all("td")[5].text
                        nb_of_rev = soup.find_all("td")[6].text
                        titres = soup.find("h1").text
                        category = soup.find_all("a")[3].text

                        for div in soup.find_all('div', class_='item active'):
                            for i in div.findAll('img'):
                                source_photo = (i['src'])
                                source_clean = source_photo.replace("../../", "https://books.toscrape.com/")
                                alt = i['alt']
                                photos = open(alt.replace(' ', '-').replace('/', '') + ".jpg", "wb")
                                try:
                                    im = requests.get(source_clean)
                                    photos.write(im.content)
                                finally:
                                    photos.close()

                        data_one_page_scrap = [url_to_scrap, upc, titres, price_inc_tax, price_exc_tax, availability, description,
                                    category, nb_of_rev, source_clean]
                        the_writer.writerow(data_one_page_scrap)
        finally:
            file_one_page_scrap.close()



        return logging.info("END OF PROGRAM")





def scraper(url_to_scrap: str, folder: str) -> str:
    """
    This function scrap all important data for society.
    this data is intended to help market research.
    all data will be saved in a corresponding folder.

    param 1 : url_to_scrap -> str
    param 2 : folder-> str

    """
    response = requests.get(url_to_scrap)
    tree = html.fromstring(response.content)
    button_next = tree.xpath("//li[@class='next']")

    if button_next and response.ok:
        logging.info(response)
        methode_scrap_pagination(url_to_scrap, folder)

    else:
        scrap_for_one_page(url_to_scrap, folder)

    return logging.info("No problem in code")



