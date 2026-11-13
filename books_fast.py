import csv
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

s = requests.Session()

def get_page(n):
    url = "https://books.toscrape.com/catalogue/page-" + str(n) + ".html"
    for attempt in range(3):
        try:
            r = s.get(url, timeout=15)
            r.raise_for_status()
            break
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for b in soup.select("article.product_pod"):
        title = b.h3.a["title"]
        price = b.select_one("p.price_color").text.strip()
        rating = b.select_one("p.star-rating")["class"][1]
        stock = b.select_one("p.instock").text.strip()
        out.append([title, price, rating, stock])
    return out

t0 = time.time()
with ThreadPoolExecutor(max_workers=5) as ex:
    pages = list(ex.map(get_page, range(1, 51)))
rows = [x for p in pages for x in p]

with open("books_fast.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["title", "price", "rating", "stock"])
    w.writerows(rows)

print(len(rows), "books saved in", round(time.time() - t0, 1), "seconds")
