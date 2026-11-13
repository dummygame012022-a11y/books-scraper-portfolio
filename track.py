import csv
import os
import sys
import datetime

src = sys.argv[1] if len(sys.argv) > 1 else "books_clean.csv"
today = datetime.date.today().isoformat()

last = {}
if os.path.exists("history.csv"):
    with open("history.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            last[(r["title"], int(r["n"]))] = float(r["price"])
first = not last

seen = {}
new_rows = []
changes = []
with open(src, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        t = r["title"]
        seen[t] = seen.get(t, 0) + 1
        k = (t, seen[t])
        p = float(r["price"])
        if k not in last:
            new_rows.append([today, t, k[1], p])
        elif last[k] != p:
            new_rows.append([today, t, k[1], p])
            changes.append((t, last[k], p))

exists = os.path.exists("history.csv")
with open("history.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if not exists:
        w.writerow(["date", "title", "n", "price"])
    w.writerows(new_rows)

if first:
    print("First run:", len(new_rows), "prices saved as baseline")
else:
    print(len(changes), "price changes found")
    for t, a, b in changes[:10]:
        print(a, "->", b, t[:50])
