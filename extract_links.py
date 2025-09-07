import csv
import urllib
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup

USER_AGENT =  "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
headers = {"User-Agent": USER_AGENT}

# 基準となるURL
url = "https://quotes.toscrape.com/"

# 相対URLに変換する
relative_url = ""

# 絶対URLに変換する
url = urljoin(url, relative_url)

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
links = [url['href'] for url in soup.find_all("a", href=True)]

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
        writer = csv.writer(f)
        for link in links:
            writer.writerow([link])
        save_path = "links.csv"
    print(f"{url}のリンクを{save_path}に保存しました。")