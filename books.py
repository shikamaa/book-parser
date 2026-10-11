from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from time import sleep
import json

page = 1

all_books = []

while True:
    print(f"Page: {page}")
    page_req = requests.get(f"https://books.toscrape.com/catalogue/page-{page}.html")
    if page_req.status_code != 200:
        print("End")
        break
    web_page = BeautifulSoup(page_req.text, "lxml")
    books = web_page.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book_number, book in enumerate(books):
        title = book.select_one("h3 > a").get("title")

        price = book.select_one("div.product_price > p.price_color").text[1::]
        availability = book.select_one(
            "div.product_price > p.instock.availability"
        ).get_text(strip=True)
        link = book.select_one("div.image_container > a").get("href")
        url = urljoin("https://books.toscrape.com/catalogue/", link)
        rating = book.select_one("p.star-rating").get("class")[1]

        current_book = {
            "name": title,
            "price": price,
            "url": url,
            "rating": rating,
            "availability": availability
        }
        all_books.append(current_book)
    
    page += 1 
    sleep(1)

with open("data.json", "w", encoding="utf-8") as file:
    json.dump({"books": all_books}, file, indent=4, ensure_ascii=False)

print("Book amount:", len(all_books))
