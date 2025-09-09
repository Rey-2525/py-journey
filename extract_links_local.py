import bs4
import csv
import argparse
from urllib.parse import urljoin
import requests
import os

parser = argparse.ArgumentParser()
parser.add_argument("htmlfile", help="HTMLファイルのパスまたはURL")
args = parser.parse_args()

# URLかファイルパスかを判定
if args.htmlfile.startswith("http://") or args.htmlfile.startswith("https://"):
    response = requests.get(args.htmlfile)
    response.raise_for_status()
    html = response.text
else:
    with open(args.htmlfile, encoding="utf-8") as f:
        html = f.read()

soup = bs4.BeautifulSoup(html, "html.parser")
links = soup.find_all("a")

csvlist = []
for link in links:
    text = link.text
    csvlist.append([text, link.get("href")])

with open("links_local.csv", "w", encoding="utf-8", newline="") as f:
    writecsv = csv.writer(f, lineterminator="\n")
    writecsv.writerows(csvlist)

save_path = "links_local.csv"
print(f"リンクを{save_path}に保存しました。")