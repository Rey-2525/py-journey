import bs4
import csv
import argparse
from urllib.parse import urljoin

base_url = "https;//example.com"
absolute_url = urljoin(base_url, "/about")
print(absolute_url)

parser = argparse.ArgumentParser()
parser.add_argument("htmlfile", help="HTMLファイルのパス")
args = parser.parse_args()
with open(args.html_path, encoding="utf-8") as f:
    soup = bs4.BeautifulSoup(f, "html.parser")
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