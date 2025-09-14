import argparse
import csv
import urllib
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup

USER_AGENT =  "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
headers = {"User-Agent": USER_AGENT}

# URLかどうかを判定する関数
def is_url(s: str) -> bool:
    scheme = urlparse(s).scheme.lower()
    return scheme in ("http", "https")

# htmlファイルの解析
parser = argparse.ArgumentParser()
parser.add_argument("htmlfile", help="HTMLファイルのパス")
args = parser.parse_args()
with open(args.htmlfile, encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

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

base_tag = soup.find("base", href=True)
base = base_tag["href"] if base_tag else None
absolute = urljoin(base, href) if base else href

# URLでなければ基準URLからの相対パスを絶対パスに変換
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
            writer.writerow([text, absolute])
        save_path = "links.csv"
    print(f"{url}のリンクを{save_path}に保存しました。")