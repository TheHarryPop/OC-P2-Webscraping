import urllib.request
import requests
import os
from bs4 import BeautifulSoup


def process():
    links_cat = []
    links_books = []
    titles = []
    extract_cat(links_cat)
    extract_books(links_books, links_cat)
    extract_data(links_books, titles)
    titres = set(titles)
    print(f"Après suppression des doubles il reste {len(titres)} titres")


def extract_cat(links_cat):

    url = "http://books.toscrape.com"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        uls = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li")

        for ul in uls:
            a = ul.find("a")
            linky = a["href"]
            link = ("http://books.toscrape.com/" + linky)
            links_cat.append(link)
            url = link.replace("index.html", "page-")
            i = 1
            response2 = requests.get(url + str(i) + ".html")

            while response2.ok:
                i += 1
                lien = url + str(i) + ".html"
                response3 = requests.get(lien)

                if response3.ok:
                    links_cat.append(lien)

                else:
                    break

        return links_cat


def extract_books(links_books, links_cat):

    for link in links_cat:
        response = requests.get(link)

        if response.ok:
            soup = BeautifulSoup(response.content, "lxml")
            lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            for li in lis:
                a = li.find("a")
                link = a["href"]
                clean = link.replace("../../../", "")
                links_books.append("http://books.toscrape.com/catalogue/" + clean)

    return links_books


def extract_data(links_books, titles):

    separator = "|"

    with open("Extraction.csv", "w", encoding="utf-8-sig") as outf:
        outf.write("product_page_url" + separator + "universal_product_code" + separator + "title" + separator +
                    "price_including_tax" + separator + "price_excluding_tax" + separator + "number_available" +
                    separator + "product_description" + separator + "category" + separator + "review_rating" +
                    separator + "image_url" + "\n")

        for lien in links_books:
            response = requests.get(lien)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")

                product_page_url = lien

                upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
                universal_product_code = upc[0].text

                title = soup.find("li", {"class": "active"}).text
                titles.append(title)

                pit = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_including_tax = pit[3].text

                pet = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_excluding_tax = pet[2].text

                na = soup.find("table", {"class": "table table-striped"}).find_all("td")
                number_available = na[5].text

                if soup.find("div", {"id": "product_description"}):
                    pd = soup.find("div", {"id": "product_description"}).findNext("p")
                    product_description = pd.text
                else:
                    product_description = "No description available"

                cat = soup.find("li", {"class": "active"}).findPrevious("a")
                category = cat.text

                if soup.find("p", {"class": "star-rating One"}):
                    review_rating = "1 Étoile"
                elif soup.find("p", {"class": "star-rating Two"}):
                    review_rating = "2 Étoiles"
                elif soup.find("p", {"class": "star-rating Three"}):
                    review_rating = "3 Étoiles"
                elif soup.find("p", {"class": "star-rating Four"}):
                    review_rating = "4 Étoiles"
                else:
                    review_rating = "5 Étoiles"

                img = soup.find("div", {"class": "item active"}).find("img")
                img_url = img["src"]
                cleaner = img_url.replace("../../", "")
                image_url = ("http://books.toscrape.com/" + cleaner)
                if not os.path.exists("C:/Users/winke/Desktop/GitHub/Webscraping/Images"):
                    os.makedirs("C:/Users/winke/Desktop/GitHub/Webscraping/Images")
                with open("C:/Users/winke/Desktop/GitHub/Webscraping/Images/" +
                          title.replace(":", "").replace("/", "").replace("\"", "").replace("*", "#").replace("?", "")
                          + ".jpg", 'wb') as image:
                    image.write(urllib.request.urlopen(image_url).read())
                image.close()

                outf.write(product_page_url + separator + universal_product_code + separator + title + separator +
                           price_including_tax + separator + price_excluding_tax + separator + number_available +
                           separator + product_description + separator + category + separator + review_rating +
                           separator + image_url + "\n")
        return titles


process()


"dans 3 fonctions"
"1 extraire cat"
"2 extraire liens des livres"
"3 extraire data avec un csv par catégorie"
"extraire les photos dans un dossier et les lier à la base de données"
