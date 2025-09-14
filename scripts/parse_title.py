import requests
from bs4 import BeautifulSoup

USER_AGENT =  "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
headers = {"User-Agent": USER_AGENT}
url = "https://www.city.ageo.lg.jp/"

ok = False
try:
    response = requests.get(url, headers=headers, timeout=(5, 15))
    response.raise_for_status()  # 4xx/5xxで例外
    soup = BeautifulSoup(response.content, "html.parser")
    title_text = soup.find("title").get_text()
    print(f"Title: {title_text}")
    print("通信成功")
    ok = True
except requests.exceptions.Timeout:
    print("タイムアウト")
except requests.exceptions.HTTPError as e:
    print(f"HTTPエラー: {e}")
except requests.exceptions.RequestException as e:
    print(f"通信エラー: {e}")
if ok:
    with open("parse.html", "w", encoding="utf-8") as f:
        f.write(soup.text)
    with open("parse_raw.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    save_path = "parse.html"
    save_path = "parse_raw.html"
    print(f"{url}を{save_path}に保存しました。")