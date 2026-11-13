import csv
import re

words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
rows = []
with open("books_fast.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        price = float(re.sub(r"[^0-9.]", "", r["price"]))
        rows.append([r["title"], price, words[r["rating"]], r["stock"]])

with open("books_clean.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["title", "price", "rating", "stock"])
    w.writerows(rows)

print(len(rows), "rows saved")
five = sorted([x for x in rows if x[2] == 5], key=lambda x: x[1])[:5]
print("5 cheapest 5-star books:")
for x in five:
    print(x[1], x[0][:60])
