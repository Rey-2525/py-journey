href と text のペアでCSV出力

- writer.writerow([link])
+ writer.writerow([link_text, absolute_href])


変数名の衝突を解消

- links = [url['href'] for url in soup.find_all("a", href=True)]
+ anchors = soup.find_all("a", href=True)
+ links = []
+ for a in anchors:
+     href = a.get("href")
+     text = a.get_text(strip=True)


相対 → 絶対URLの解決（urljoin）

基準URL（base）は以下の優先順で決める：

<base href="..."> がHTML内にあればそれ（soup.find("base", href=True)）

コマンドライン引数で --base-url を渡せるように（元ページURLがわかる場合）

どれもなければ そのまま（相対のまま） だが、実務では(1) or (2)推奨

+ from urllib.parse import urljoin
+ base = base_from_html_or_arg  # 1 or 2 の方法で決定
+ absolute = urljoin(base, href) if base else href


不要/未使用コードの整理

- relative_url = ""
- url = urljoin(url, relative_url)


（この2行は意味を生んでいないので削除）

extract_links

空href/無効スキームをスキップ

if not href: continue
if href.startswith(("javascript:", "mailto:", "#")): continue


重複除去（順序維持）

集合で既出hrefを管理してスキップ（seen = set() → if in seen: continue → add）

CSVヘッダとUTF-8

- writer = csv.writer(f)
+ writer = csv.writer(f, lineterminator="\n")
+ writer.writerow(["text", "href"])


CLI引数で入力ファイル & 基準URL

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("html_path")
parser.add_argument("--base-url", default=None)
args = parser.parse_args()


実行例：

python extract_links.py parse_raw.html --base-url https://quotes.toscrape.com/


例外処理（ファイル/パース系）

FileNotFoundError / UnicodeDecodeError を握って、ユーザに原因を出力

読み込みは encoding="utf-8"（必要なら errors="ignore" で一時回避）

処理結果の要約表示

「総リンク数 / 保存件数（重複・無効除外後）」を print で出す
