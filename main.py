import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)

with open("Étape 1.csv", "w") as outf:
    outf.write("product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, "
               "number_available, product_description, category, review_rating, image_url\n")
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
    # extract url ok
        product_page_url = url
    # extract UPC ok
        upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
        universal_product_code = upc[0]
    # extract title ok
        title = soup.find("li", {"class": "active"})
    # extract PIT ok
        pit = soup.find("table", {"class": "table table-striped"}).find_all("td")
        price_including_tax = pit[3]
    # extract PET ok
        pet = soup.find("table", {"class": "table table-striped"}).find_all("td")
        price_excluding_tax = pet[2]
    # extract na ok
        na = soup.find("table", {"class": "table table-striped"}).find_all("td")
        number_available = na[5]
    # pourquoi n'affiche pas "p" ?
        product_description = soup.find("div", {"id": "product_description"}).findNext("p")
    # extract category ok
        category = soup.find("li", {"class": "active"}).findPrevious("a")
    # extract rr ok
        rr = soup.find("table", {"class": "table table-striped"}).find_all("td")
        review_rating = rr[6]
    # extract img_url ok
        img = soup.find("div", {"class": "item active"}).find("img")
        image_url = img["src"]

        outf.write(product_page_url + "," + universal_product_code.text + "," + title.text + "," +
                   price_including_tax.text + "," + price_excluding_tax.text + "," + number_available.text + ","
                   + product_description.text + "," + category.text + "," + review_rating.text + str(image_url) + "\n")
