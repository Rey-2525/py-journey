import argparse
import csv
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
    parser.add_argument(
        "--out",
        help="出力CSVファイル名",
        default="output.csv",
    )
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
    saved = 0
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["text", "href"])  # ヘッダー行
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
            writer.writerow([link_text, absolute_url])
            saved += 1
            if saved == 0:
                print("links=0")
            else:
                print(f"抽出:{len(links)} 保存:{saved} → {args.out}")

            print(f"抽出:{link_text} | {absolute_url} 保存:{saved} → output.csv")


# 実行部分
if __name__ == "__main__":
    main()
