import csv
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

base = "https://books.toscrape.com/catalogue/page-1.html"
r = requests.get(base, timeout=15)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")
cats = [urljoin(base, a["href"]) for a in soup.select("div.side_categories ul li ul li a")]
print(len(cats), "categories found", flush=True)
rows = []
for curl in cats:
    url = curl
    name = ""
    n = 0
    while url:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        r.encoding = "utf-8"
        s = BeautifulSoup(r.text, "html.parser")
        name = s.h1.text.strip()
        for b in s.select("article.product_pod"):
            rows.append([b.h3.a["title"], name])
            n += 1
        nxt = s.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(0.3)
    print(name, n, flush=True)

with open("categories.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["title", "category"])
    w.writerows(rows)

print(len(rows), "rows saved")
