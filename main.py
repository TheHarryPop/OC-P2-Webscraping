import requests
from bs4 import BeautifulSoup

links_cat = []
links_books = []


def test():
    links1 = []
    links2 = []
    links3 = []

    for link in links_cat:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "lxml")

        if soup.find("li", {"class": "next"}):

            a = soup.find("li", {"class": "next"}).find("a")
            link1 = link.replace("index.html", a["href"])
            links1.append(link1)

    for link2 in links1:
        response2 = requests.get(link2)
        soup2 = BeautifulSoup(response2.text, "lxml")

        if soup2.find("li", {"class": "next"}):
            a2 = soup2.find("li", {"class": "next"}).find("a")
            link3 = link2.replace("page-2.html", a2["href"])
            links2.append(link3)

    for link3 in links2:
        response3 = requests.get(link3)
        soup3 = BeautifulSoup(response3.text, "lxml")

        if soup3.find("li", {"class": "next"}):
            a3 = soup3.find("li", {"class": "next"}).find("a")
            link4 = link3.replace("page-3.html", a3["href"])
            links3.append(link4)

    links2.extend([links3])
    links1.extend([links2])
    print(links1)


def extract_cat():

    url = "http://books.toscrape.com"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        uls = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li")

        for ul in uls:
            a = ul.find("a")
            link = a["href"]
            links_cat.append("http://books.toscrape.com/" + link)


def extract_books():

    for link in links_cat:
        response = requests.get(link)

        if response.ok:
            soup = BeautifulSoup(response.text, "lxml")
            lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            for li in lis:
                a = li.find("a")
                link = a["href"]
                clean = link.replace("../../../", "")
                links_books.append("http://books.toscrape.com/catalogue/" + clean)


extract_cat()
test()
# extract_books()

# links = []
#
# for i in range(1, 3, 1):
#     url = "http://books.toscrape.com/catalogue/category/books/mystery_3/page-" + str(i) + ".html"
#     response = requests.get(url)
#
#     if response.ok:
#         soup = BeautifulSoup(response.text, "lxml")
#         lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
#
#         for li in lis:
#             a = li.find("a")
#             link = a["href"]
#             clean = link.replace("../../../", "")
#             links.append("http://books.toscrape.com/catalogue/" + clean)

# with open("Étape 2.csv", "w") as outf:
#     outf.write("product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,"
#                "number_available, product_description, category, review_rating, image_url \n")
#
#     for lien in links:
#         response = requests.get(lien)
#         if response.ok:
#             soup = BeautifulSoup(response.text, "lxml")
#
#             product_page_url = lien
#
#             upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
#             universal_product_code = upc[0]
#
#             title = soup.find("li", {"class": "active"})
#
#             pit = soup.find("table", {"class": "table table-striped"}).find_all("td")
#             price_including_tax = pit[3].text.replace("Â", "")
#
#             pet = soup.find("table", {"class": "table table-striped"}).find_all("td")
#             price_excluding_tax = pet[2].text.replace("Â", "")
#
#             na = soup.find("table", {"class": "table table-striped"}).find_all("td")
#             number_available = na[5]
#
#             product_description = str(soup.find("div", {"id": "product_description"}).findNext("p").next).encode("utf-8")
#
#             category = soup.find("li", {"class": "active"}).findPrevious("a")
#
#             rr = soup.find("table", {"class": "table table-striped"}).find_all("td")
#             review_rating = rr[6]
#
#             img = soup.find("div", {"class": "item active"}).find("img")
#             img_url = img["src"]
#             cleaner = img_url.replace("../../", "")
#             image_url = ("http://books.toscrape.com/" + cleaner)
#
#             outf.write(product_page_url + "," + universal_product_code.text + "," + title.text + "," +
#                        price_including_tax + "," + price_excluding_tax + "," + number_available.text + ","
#                        + str(product_description)
#                        + "," + category.text + "," + review_rating.text + "," + image_url + "\n")


"dans 3 fonctions" \
"1 extraire cat" \
"2 extraire liens des livres" \
"3 extraire data"