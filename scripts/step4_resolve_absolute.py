import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin


# URLかどうかを判定する関数
def is_url(s: str) -> bool:
    return urlparse(s).scheme in ("http", "https")


# URLからテキストを読み込む
def read_text_from_url(url: str) -> str:
    import requests

    resp = requests.get(url, timeout=(5, 15))
    resp.raise_for_status()
    return resp.text


# ローカルファイルからテキストを読み込む
def read_text_from_file(filepath: str) -> str:
    with open(filepath, encoding="utf-8") as f:
        return f.read()


# パーサーで引数を処理し、URLかファイルかを判定して読み込む
def main():
    parser = argparse.ArgumentParser(description="URLまたはファイルを読み込む")
    parser.add_argument("input", help="URLまたはローカルファイルパス")
    args = parser.parse_args()

    if is_url(args.input):
        kind = "URL"
        text = read_text_from_url(args.input)
    else:
        kind = "FILE"
        text = read_text_from_file(args.input)

    if kind == "URL":
        base_url = args.input
    else:
        base_url = None

    soup = BeautifulSoup(text, "html.parser")
    links = soup.find_all("a", href=True) or []

    # <base>タグがあれば優先
    base_tag = soup.find("base", href=True)
    if base_tag:
        base_url = base_tag["href"]

    seen = set()
    count = 0
    for a in links:
        href = a.get("href")
        if not href:
            continue
        if href.startswith(("javascript:", "mailto:", "#")):
            continue
        link_text = a.get_text(strip=True)
        # 絶対URLに変換
        absolute_url = href
        if base_url:
            absolute_url = urljoin(base_url, href)
        # 重複排除
        if absolute_url in seen:
            continue
        seen.add(absolute_url)
        print(f"{link_text} | {absolute_url}")
        count += 1
        if count == 5:
            break

    if count == 0:
        print("links=0")
    else:
        print(f"links={count}")


# 実行部分
if __name__ == "__main__":
    main()
