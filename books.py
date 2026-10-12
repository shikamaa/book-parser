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
    if page_req.status_code == 404:
        print("End.")
        break
    web_page = BeautifulSoup(page_req.text, "lxml")
    books = web_page.find_all("article", class_="product_pod")

    for book_number, book in enumerate(books):
        current_book = {
            "name": book.select_one("h3 > a").get("title"),
            "price": float(book.select_one("p.price_color").get_text(strip=True).lstrip("Â£")),
            "url": urljoin("https://books.toscrape.com/catalogue/", book.select_one("div.image_container > a").get("href")),
            "rating": book.select_one("p.star-rating").get("class")[1],
            "availability": book.select_one(
            "div.product_price > p.instock.availability"
        ).get_text(strip=True)
        }
        all_books.append(current_book)
    
    page += 1 
    sleep(1)

with open("data.json", "w", encoding="utf-8") as file:
    json.dump({"books": all_books}, file, indent=4, ensure_ascii=False)

print("Book amount:", len(all_books))