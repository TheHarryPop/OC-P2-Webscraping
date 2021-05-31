import requests
from bs4 import BeautifulSoup


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


def extract_books(links_books):

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


def extract_data():

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
                print(title)

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
                print(category)

                rr = soup.find("table", {"class": "table table-striped"}).find_all("td")
                review_rating = rr[6].text

                img = soup.find("div", {"class": "item active"}).find("img")
                img_url = img["src"]
                cleaner = img_url.replace("../../", "")
                image_url = ("http://books.toscrape.com/" + cleaner)

                outf.write(product_page_url + separator + universal_product_code + separator + title + separator +
                           price_including_tax + separator + price_excluding_tax + separator + number_available +
                           separator + product_description + separator + category + separator + review_rating +
                           separator + image_url + "\n")


def process():
    links_cat = []
    links_books = []
    extract_cat(links_cat)
    # extract_books(links_books)
    # extract_data()

process()


"dans 3 fonctions"
"1 extraire cat"
"2 extraire liens des livres"
"3 extraire data avec un csv par catégorie"
"extraire nombre d'étoiles"
"Mettre titres dans set (video) = 999 titres différents"
