import urllib.request
import requests
import os
import csv
from bs4 import BeautifulSoup


def process():
    titles = []
    extract_cat()
    titles.append(extract_data(titles))
    titres = set(titles)
    print(f"Après suppression des doubles il reste {len(titres)} titres")


def extract_cat():

    url = "http://books.toscrape.com"
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, "lxml")
        uls = soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li")

        for ul in uls:
            links_cat = []
            a = ul.find("a")
            linky = a["href"]
            cat = a.text.replace("\n", "").replace(" ", "")
            cat = category_correction(cat)
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
            links_books = extract_books(links_cat)
            extract_data(links_books, cat)


def extract_books(links_cat):
    links_books = []

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


def extract_data(links_books, cat):

    separator = "|"
    titles = []

    if not os.path.exists("./CSV"):
        os.makedirs("./CSV")

    with open("./CSV/" + cat + ".csv", "w", encoding="utf-8-sig", newline="") as outf:
        writer = csv.writer(outf, delimiter="|")
        outf.write("product_page_url" + separator + "universal_product_code" + separator + "title" + separator +
                   "price_including_tax" + separator + "price_excluding_tax" + separator + "number_available" +
                   separator + "product_description" + separator + "category" + separator + "review_rating" +
                   separator + "image_url" + "\n")

        for lien in links_books:
            data = []
            response = requests.get(lien)
            if response.ok:
                soup = BeautifulSoup(response.content, "html.parser")

                product_page_url = lien
                data.append(product_page_url)

                upc = soup.find("table", {"class": "table table-striped"}).find_all("td")
                universal_product_code = upc[0].text
                data.append(universal_product_code)

                title = soup.find("li", {"class": "active"}).text
                data.append(title)
                titles.append(title)

                pit = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_including_tax = pit[3].text
                data.append(price_including_tax)

                pet = soup.find("table", {"class": "table table-striped"}).find_all("td")
                price_excluding_tax = pet[2].text
                data.append(price_excluding_tax)

                na = soup.find("table", {"class": "table table-striped"}).find_all("td")
                number_available = na[5].text
                data.append(number_available)

                if soup.find("div", {"id": "product_description"}):
                    pd = soup.find("div", {"id": "product_description"}).findNext("p")
                    product_description = pd.text
                    data.append(product_description)
                else:
                    product_description = "No description available"
                    data.append(product_description)

                cate = soup.find("li", {"class": "active"}).findPrevious("a")
                category = cate.text
                data.append(category)

                if soup.find("p", {"class": "star-rating One"}):
                    review_rating = "1 Étoile"
                    data.append(review_rating)
                elif soup.find("p", {"class": "star-rating Two"}):
                    review_rating = "2 Étoiles"
                    data.append(review_rating)
                elif soup.find("p", {"class": "star-rating Three"}):
                    review_rating = "3 Étoiles"
                    data.append(review_rating)
                elif soup.find("p", {"class": "star-rating Four"}):
                    review_rating = "4 Étoiles"
                    data.append(review_rating)
                elif soup.find("p", {"class": "star-rating Five"}):
                    review_rating = "5 Étoiles"
                    data.append(review_rating)
                else:
                    review_rating = "Il n'y a pas de note"
                    data.append(review_rating)

                img = soup.find("div", {"class": "item active"}).find("img")
                img_url = img["src"]
                cleaner = img_url.replace("../../", "")
                image_url = ("http://books.toscrape.com/" + cleaner)
                data.append(image_url)
                if not os.path.exists("./Images"):
                    os.makedirs("./Images")
                with open("./Images/" +
                          title.replace(":", "").replace("/", "").replace("\"", "").replace("*", "#").replace("?", "").replace(" ", "_")
                          + ".jpg", 'wb') as image:
                    image.write(urllib.request.urlopen(image_url).read())
                writer.writerow(data)
    return titles


def category_correction(cat):
    if cat == "HistoricalFiction":
        cat = "Historical Fiction"
    elif cat == "SequentialArt":
        cat = "Sequential Art"
    elif cat == "WomensFiction":
        cat = "Womens Fiction"
    elif cat == "Nonfiction":
        cat = "Non fiction"
    elif cat == "ScienceFiction":
        cat = "Science Fiction"
    elif cat == "SportsandGames":
        cat = "Sports and Games"
    elif cat == "Addacomment":
        cat = "Add a comment"
    elif cat == "NewAdult":
        cat = "New Adult"
    elif cat == "YoungAdult":
        cat = "Young Adult"
    elif cat == "AdultFiction":
        cat = "Adult Fiction"
    elif cat == "FoodandDrink":
        cat = "Food and Drink"
    elif cat == "ChristianFiction":
        cat = "Christian Fiction"
    elif cat == "SelfHelp":
        cat = "Self Help"
    elif cat == "ShortStories":
        cat = "Short Stories"
    return cat


process()
