import argparse
import csv
import urllib
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup

USER_AGENT =  "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
headers = {"User-Agent": USER_AGENT}

parser = argparse.ArgumentParser()
parser.add_argument("html_path")
parser.add_argument("--base-url", default=None)
args = parser.parse_args()

# 基準となるURL
url = "https://quotes.toscrape.com/"

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
anchors = soup.find_all("a", href=True)
links = []
for a in anchors:
    href = a["href"]
    text = a.get_text(strip=True)
    if not href:
        continue
    if href.startswith("javascript:", "mailto","#"):
        continue
    
base = args.base_url
absolute = urljoin(base, href) if base else href

ok = False
try:
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=10) as response:
        if response.status == 200:
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            links = [url['href'] for url in soup.find_all("a", href=True)]
            print("通信成功")
    ok = True
except FileNotFoundError as e:
    print(f"ファイルが見つかりません: {e}")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
except HTTPError as e:
    print(f"HTTPエラー: {e}")
except URLError as e:
    print(f"URLエラーが発生しました。: {e}")
if ok:
    with open("links.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        for link in links:
            writer.writerow(["text", "href"])
        save_path = "links.csv"
    print(f"{url}のリンクを{save_path}に保存しました。")