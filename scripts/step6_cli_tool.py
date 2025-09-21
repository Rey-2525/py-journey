import argparse
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin

USERAgent = "(Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100)"
headers = {"User-Agent": USERAgent}


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


# パーサーで引数を処理する関数
def parse_argument():
    parser = argparse.ArgumentParser(description="URLまたはファイルを読み込む")
    parser.add_argument("input", help="URLまたはローカルファイルパス")
    parser.add_argument(
        "--out",
        help="出力CSVファイル名",
        default="output.csv",
    )
    args = parser.parse_args()
    return args


# URLかファイルかを判定して読み込む関数
def url_or_file(args):
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
    return text, base_url


# リンクを抽出する関数
def extract_links(text, base_url):
    soup = BeautifulSoup(text, "html.parser")
    links = []
    base_tag = soup.find("base", href=True)
    if base_tag:
        base_url = base_tag["href"]
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if href and not href.startswith(("javascript:", "mailto:", "#")):
            absolute_url = urljoin(base_url, href) if base_url else href
            link_text = a.get_text(strip=True)
            links.append((link_text, absolute_url))
    return links


# 重複排除する関数
def remove_duplicates(links):
    seen = set()
    for text, url in links:
        if url not in seen:
            seen.add(url)
            yield text, url


# リンクをCSVに保存する関数
def save_links_to_csv(links, args):
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "href"])
        for text, url in links:
            writer.writerow([text, url])


def main():
    args = parse_argument()
    text, base_url = url_or_file(args)
    links = extract_links(text, base_url)
    unique_links = remove_duplicates(links)
    save_links_to_csv(unique_links, args.out)


# 実行部分
if __name__ == "__main__":
    main()
