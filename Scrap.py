# coding:utf-8


import requests as r
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urljoin
import csv
import os


def scrapPage(url_P, folder):
    res = r.get(url_P)
    soup = BeautifulSoup(res.content, "lxml")
    tree = html.fromstring(res.content)
    para = tree.xpath("//li[@class='next']")




    if para:   ###condition pour vérifier si un boutton next est disponnible###
        print("        Boutton 'Next' dectecté        ", "\n")
        os.mkdir(os.path.join(os.getcwd(), folder))
        try:
            os.chdir(os.path.join(os.getcwd(), folder))
            with open('dataScrap.csv', 'w', encoding='utf-8',
                      newline='') as f:  ###fonction pour crée le fichier csv et crée les colonnes correspondante###

                thwriter = csv.writer(f, delimiter=str(';'))
                header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                          'price_excluding_tax',
                          'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                thwriter.writerow(header)

                ###Boucle pour naviguer dans tout les pages###
                while True:

                    res = r.get(url_P)
                    soup = BeautifulSoup(res.content, "lxml")

                    footer_element = soup.select_one('li.current')
                    print(footer_element.text.strip())

                    ###Trouver la page suivante a Scrapper dans la pagination###
                    next_page_element = soup.select_one('li.next > a')
                    last_page = soup.select_one('li.previous> a')

                    if next_page_element:
                        next_page_url = next_page_element.get('href')
                        url_P = urljoin(url_P, next_page_url)
                        if url_P:
                            for url in soup.findAll('div', class_='image_container'):
                                data = url.findAll('a', href=True)
                                for links in data:
                                    href = links.get("href")
                                    link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                                    tbl = {link}
                                    for scrap in tbl:
                                        res = r.get(scrap)
                                        soup = BeautifulSoup(res.content, "lxml")
                                        tree = html.fromstring(res.content)

                                        for para in soup.findAll('article', class_='product_page'):
                                            description = soup.find_all("p")[3].text

                                        uPC = soup.find_all("td")[0].text
                                        price_exc = soup.find_all("td")[2].text
                                        price_inc = soup.find_all("td")[3].text
                                        availability = soup.find_all("td")[5].text
                                        nb_of_rev = soup.find_all("td")[6].text

                                        for titre in soup.findAll('div', class_='col-sm-6 product_main'):
                                            titres = soup.find("h1").text

                                        for section in soup.findAll('ul', class_='breadcrumb'):
                                            category = soup.find_all("a")[3].text


                                        for div in soup.find_all('div', class_='item active'):
                                            img = div.findAll('img')
                                            for i in img:
                                                source_photo = (i['src'])
                                                source_clean = source_photo.replace("../../",
                                                                                    "https://books.toscrape.com/")
                                                alt = i['alt']

                                                with open(alt.replace(' ', '-').replace('/', '') + ".jpg",
                                                          "wb") as fotos:
                                                    im = r.get(source_clean)
                                                    fotos.write(im.content)

                                        ###valeur du scrap pour chaque colonnes correspondante###
                                        info = [link,
                                                uPC,
                                                titres,
                                                price_inc,
                                                price_exc,
                                                availability,
                                                description,
                                                category,
                                                nb_of_rev,
                                                source_clean]
                                        thwriter.writerow(info)

                    else:
                        for url in soup.findAll('div', class_='image_container'):
                            data = url.findAll('a', href=True)
                            for links in data:
                                href = links.get("href")
                                link = href.replace("../../..", "https://books.toscrape.com/catalogue")
                                tbl = {link}
                                for scrap in tbl:
                                    res = r.get(scrap)
                                    soup = BeautifulSoup(res.content, "lxml")
                                    tree = html.fromstring(res.content)

                                    for para in soup.findAll('article', class_='product_page'):
                                        description = soup.find_all("p")[3].text

                                    uPC = soup.find_all("td")[0].text
                                    price_exc = soup.find_all("td")[2].text
                                    price_inc = soup.find_all("td")[3].text
                                    availability = soup.find_all("td")[5].text
                                    nb_of_rev = soup.find_all("td")[6].text

                                    for titre in soup.findAll('div', class_='col-sm-6 product_main'):
                                        titres = soup.find("h1").text

                                    for section in soup.findAll('ul', class_='breadcrumb'):
                                        category = soup.find_all("a")[3].text



                                    for div in soup.find_all('div', class_='item active'):
                                        img = div.findAll('img')
                                        for i in img:
                                            source_photo = (i['src'])
                                            source_clean = source_photo.replace("../../", "https://books.toscrape.com/")
                                            alt = i['alt']
                                            with open(alt.replace(' ', '-').replace('/', '') + ".jpg", "wb") as fotos:
                                                im = r.get(source_clean)
                                                fotos.write(im.content)

                                    ###valeur du scrap pour chaque colonnes correspondante###
                                    info = [link,
                                            uPC,
                                            titres,
                                            price_inc,
                                            price_exc,
                                            availability,
                                            description,
                                            category,
                                            nb_of_rev,
                                            source_clean]
                                    thwriter.writerow(info)

                        print("     Scrapping Sauvegardé dans le CSV du dossier     ")

                        break
        except ValueError:
            pass

    else:
        ###Essai de vérification de page sans pagination###
        try:
            os.mkdir(os.path.join(os.getcwd(), folder))
            if res.ok:

                os.chdir(os.path.join(os.getcwd(), folder))
                with open('Scrap0nePage.csv', 'w', encoding='utf-8', newline='') as f:


                    thwriter = csv.writer(f, delimiter=str(';'))
                    header = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax',
                              'price_excluding_tax',
                              'number_available', 'product_description', 'category', 'review_rating', 'image_url']
                    thwriter.writerow(header)

                    print("        Aucun boutton 'Next'        ","\n")
                    for art in soup.findAll('div', class_='image_container'):
                        lien = art.findAll('a', href=True)
                        for liens in lien:
                            href = liens.get("href")
                            link_one_page = href.replace("../../..", "https://books.toscrape.com/catalogue")
                            table = {link_one_page}
                        for scrap in table:
                            res = r.get(scrap)
                            soup = BeautifulSoup(res.content, "lxml")
                            tree = html.fromstring(res.content)
                            para = tree.xpath("//li[@class='next']")

                        for para in soup.findAll('article', class_='product_page'):
                            description = soup.find_all("p")[3].text

                        uPC = soup.find_all("td")[0].text
                        price_exc = soup.find_all("td")[2].text
                        price_inc = soup.find_all("td")[3].text
                        availability = soup.find_all("td")[5].text
                        nb_of_rev = soup.find_all("td")[6].text

                        for titre in soup.findAll('div', class_='col-sm-6 product_main'):
                            titres = soup.find("h1").text

                        for section in soup.findAll('ul', class_='breadcrumb'):
                            category = soup.find_all("a")[3].text



                        for div in soup.find_all('div', class_='item active'):
                                img = div.findAll('img')
                                for i in img:
                                    source_photo = (i['src'])
                                    source_clean = source_photo.replace("../../", "https://books.toscrape.com/")
                                    alt = i['alt']
                                    with open(alt.replace(' ', '-').replace('/', '') + ".jpg","wb") as fotos:
                                        im = r.get(source_clean)
                                        fotos.write(im.content)







                        info = [url_P, uPC,
                                titres,
                                price_inc,
                                price_exc,
                                availability,
                                description,
                                category,
                                nb_of_rev,
                                source_clean
                                ]
                        thwriter.writerow(info)

                    print("        ScrappingOnePAge Sauvegardé dans le CSV du dossier        ", "\n")



        except ValueError:
            print('il y as une ERREUR dans la boucle With', "\n")




    return print("                                          FIN DU PROGRAMME")


scrapPage("https://books.toscrape.com/catalogue/category/books/childrens_11/index.html", "children")













def scrapOneProduct(url_P):


    ##Request  the webSite
    res = r.get(url_P)
    soup = BeautifulSoup(res.text, "html.parser")
    tree = html.fromstring(res.content)
    # print(res.status_code)

    #####Get Data from Website######
    if res.ok:

        for para in soup.findAll('article', class_='product_page'):
            description = soup.find_all("p")[3].text


        uPC = soup.find_all("td")[0].text
        price_exc = soup.find_all("td")[2].text
        price_inc = soup.find_all("td")[3].text
        availability = soup.find_all("td")[5].text
        nb_of_rev = soup.find_all("td")[6].text
        title = tree.xpath("//li[@class='active']/text()")
        category = tree.xpath("/html[1]/body[1]/div[1]/div[1]/ul[1]/li[3]/a[1]/text()")

        for img in soup.findAll('img'):
            photo = img.get('src')



        d = {'product_page_url': [url_P],
             'universal_ product_code': [uPC],
             'title': [title],
             'price_including_tax': [price_inc],
             'price_excluding_tax': [price_exc],
             'number_available': [availability],
             'product_description': [para],
             'category': [category],
             'review_rating': [nb_of_rev],
             'image_url': [photo]

             }

        df = pd.DataFrame(d, columns=(
        'product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax',
        'number_available', 'product_description', 'category', 'review_rating', 'image_url'))
        df.reset_index(inplace=True)
        df.to_csv('ScrapOneProduct.csv', sep=';')

    return


#scrapOneProduct("https://books.toscrape.com/catalogue/soumission_998/index.html")
