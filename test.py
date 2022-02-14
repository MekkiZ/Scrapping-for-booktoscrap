import logging
import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urljoin
import csv
import os



def methode_scrap(url_to_scrap, folder):
                response = requests.get(url_to_scrap)
                soup = BeautifulSoup(response.content, "lxml")

                data_scv = open('dataScrap.csv', 'w', encoding='utf-8', newline='')
                try:
                    the_writer = csv.writer(data_scv, delimiter=str(';'))
                    header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                              'price_excluding_tax',
                              'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                    the_writer.writerow(header)
                    for url in soup.findAll('div', class_='image_container'):
                        for links in url.findAll('a', href=True):
                            href = links.get("href")
                            methode_scrap.link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                            tbl = {methode_scrap.link}
                            for scrap in tbl:
                                soup = BeautifulSoup(requests.get(scrap).content, "lxml")

                                methode_scrap.description = soup.find_all("p")[3].text
                                methode_scrap.upc = soup.find_all("td")[0].text
                                methode_scrap.price_exc_tax = soup.find_all("td")[2].text
                                methode_scrap.price_inc_tax = soup.find_all("td")[3].text
                                methode_scrap.availability = soup.find_all("td")[5].text
                                methode_scrap.nb_of_rev = soup.find_all("td")[6].text
                                methode_scrap.titres = soup.find("h1").text
                                methode_scrap.category = soup.find_all("a")[3].text

                                for div in soup.find_all('div', class_='item active'):
                                    for img in div.findAll('img'):
                                        alt = img['alt']
                                        methode_scrap.source_clean = img['src'].replace("../../", "https://books.toscrape.com/")
                                        photo_firsts_page = open(alt.replace(' ', '-').replace('/', '') + ".jpg",
                                                                 "wb")
                                        try:
                                            im = requests.get(methode_scrap.source_clean)
                                            photo_firsts_page.write(im.content)
                                        finally:
                                            photo_firsts_page.close()
                                ifo = [methode_scrap.link, methode_scrap.upc, methode_scrap.titres,
                                       methode_scrap.price_inc_tax,
                                       methode_scrap.price_exc_tax, methode_scrap.availability,
                                       methode_scrap.description, methode_scrap.category, methode_scrap.nb_of_rev,
                                       methode_scrap.source_clean]
                                the_writer.writerow(ifo)
                finally:
                    data_scv.close()

                return





def scraper(url_to_scrap: str, folder: str) -> str:
    response = requests.get(url_to_scrap)
    tree = html.fromstring(response.content)
    button_next = tree.xpath("//li[@class='next']")
    # condition to check if the Next button is available
    logging.info("        Bouton 'Next' detected AND Response: OK       ")

    if button_next:

            try:
                # Creat path's folder, the file CSV and Photo are there.
                os.mkdir(os.path.join(os.getcwd(), folder))
            except ValueError:
                logging.debug("Path can't creat")

            os.chdir(os.path.join(os.getcwd(), folder))

            while True:

                response = requests.get(url_to_scrap)
                soup = BeautifulSoup(response.content, "lxml")
                footer_element = soup.select_one('li.current')
                logging.info(footer_element.text.strip())

                # Find next page for pagination
                next_page_element = soup.select_one('li.next > a')
                if next_page_element and response.ok:
                    next_page_url = next_page_element.get('href')
                    url_to_scrap = urljoin(url_to_scrap, next_page_url)
                    if url_to_scrap:

                        methode_scrap(url_to_scrap, folder)

                    else:

                        methode_scrap(url_to_scrap, folder)

                        logging.info("     Scrapping as been saved     ")
                break

    else:

            methode_scrap(url_to_scrap, folder)




    return logging.info("END OF PROGRAM")
