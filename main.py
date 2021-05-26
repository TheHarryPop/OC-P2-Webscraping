import requests
from bs4 import BeautifulSoup

links = []

for i in range(1, 3, 1):
    url = "http://books.toscrape.com/catalogue/category/books/mystery_3/page-" + str(i) + ".html"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        lis = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        for li in lis:
            a = li.find("a")
            link = a["href"]
            clean = link.replace("../../../", "")
            links.append("http://books.toscrape.com/catalogue/" + clean)

with open("url.txt", "w") as file:
    for link in links:
        file.write(link + "\n")

with open("url.txt", "r") as file:
    with open("Étape 2.csv", "w") as outf:
        outf.write("product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,"
                   "number_available, product_description, category, review_rating, image_url \n")

        for row in file:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, "lxml")

                product_page_url = url

                upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
                universal_product_code = upc[0]

                title = soup.find("li", {"class": "active"})

                pit = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_including_tax = pit[3].text.replace("Â", "")

                pet = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_excluding_tax = pet[2].text.replace("Â", "")

                na = soup.find("table", {"class": "table table-striped"}).find_all("td")
                number_available = na[5]

                product_description = soup.find("div", {"id": "product_description"}).findNext("p")

                category = soup.find("li", {"class": "active"}).findPrevious("a")

                rr = soup.find("table", {"class": "table table-striped"}).find_all("td")
                review_rating = rr[6]

                img = soup.find("div", {"class": "item active"}).find("img")
                image_url = img["src"]

                outf.write(product_page_url + "," + universal_product_code.text + "," + title.text + "," +
                           price_including_tax + "," + price_excluding_tax + "," + number_available.text
                           + ","
                           # + product_description.text
                           + "," + category.text + "," + review_rating.text +
                           str(image_url) + "\n")
