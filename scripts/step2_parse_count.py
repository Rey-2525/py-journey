import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse


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

    soup = BeautifulSoup(text, "html.parser")
    links = soup.find_all("a", href=True)

    print(f"source={kind}, links={len(links)}")


# 実行部分
if __name__ == "__main__":
    main()
